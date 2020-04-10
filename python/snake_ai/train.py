import random
from model import *
from game import *
from utils import *

REINFORCE = 'REINFORCE'
ACTOR_CRITIC = 'ACTOR_CRITIC'
Q_BASIC = 'Q_BASIC'

def train(state_size, num_actions, exploration_rate=.1, discount_rate=.9, lr=.005, num_epochs=10, mode=REINFORCE, batch_size=100, load=False):
    if (exploration_rate != 0) and (mode in [REINFORCE, ACTOR_CRITIC]):
        print("================WARNING================")
        print("using non-zero exploration with a reinforce agent is weird")
    # agent and environment
    actor = Actor(state_size, num_actions).to(device)
    actor_optimizer = torch.optim.Adam(actor.parameters(), lr=lr/10)
    critic = Critic(state_size, num_actions).to(device)
    critic_loss = nn.MSELoss()
    critic_optimizer = torch.optim.Adam(critic.parameters(), lr=lr)
    if load:
        actor = load_model('actor')
        critic = load_model('critic')
    
    memory = [] # [(state, action index, next state, reward), ...]

    def batch_action(action):
        return torch.tensor([action]).long().to(device)

    def update_critic(state, action_index, nextState, reward):
        value = critic(state, action_index)

        # find best next move according to critic
        max_next_action = batch_action(0)
        max_next_value = critic(nextState, batch_action(0))
        for next_action in range(1, num_actions):
            next_action = batch_action(next_action)
            next_value = critic(nextState, next_action)
            if next_value > max_next_value:
                max_next_action = next_action
                max_next_value = next_value

        # update critic
        critic.zero_grad()
        truth = max_next_value * discount_rate + reward
        loss = critic_loss(value, truth)
        loss.backward()
        critic_optimizer.step()
        return loss.item()

    def run_episode(show=False):
        '''
        play the game and remember what happened
        '''
        game = Game(10,10)
        # playing vars
        state = state_to_tensor(game.return_state())
        reward = 0
        gameOver = False

        actor_losses = []
        critic_losses = []

        action_logprobs = []
        rewards = [] # only rewards from the actor's moves
        qs = [] # predicted rewards from the critic
        for t in range(200):
            if show:
                print()
                print(game)
            # play an episode
            if gameOver:
                break
            if mode in [REINFORCE, ACTOR_CRITIC]:
                action_logprob, action_index = actor.choose_action(state)
                should_explore = random.random() < exploration_rate
            elif mode == Q_BASIC:
                action_index = critic.choose_action(state)
            if should_explore:
                # sometimes, do a random action just to see what happens
                action_logprob, action_index = torch.tensor(1 / num_actions).to(device), batch_action(random.randint(0, num_actions-1))
            # observe next state and collect reward
            reward, nextState, gameOver = game.move_player(action_index)
            nextState = state_to_tensor(nextState)
            q = critic(state, action_index)
            
            critic_loss = update_critic(state, action_index, nextState, reward)
            critic_losses.append(critic_loss)

            if not should_explore:
                # backprop rewards to actor
                rewards.append(reward)
                if mode in [REINFORCE, ACTOR_CRITIC]:
                    logprob = action_logprob
                    action_logprobs.append(logprob)
                qs.append(q)
                
            # remember what just happened
            memory.append((state, action_index, nextState, reward))
            # update state
            state = nextState
        # replay memories for actor
        values = [] # future-discounted rewards
        discounted_actor_losses = []
        R = 0
        if mode in [REINFORCE, ACTOR_CRITIC]:
            if mode == ACTOR_CRITIC:
                rewards = qs
            for reward in rewards[::-1]:
                R = reward + discount_rate * R
                values.insert(0,R)
            for logprob, value in zip(action_logprobs, values):
                actor.zero_grad()
                score = logprob * (value.detach())
                loss = -score
                loss.backward()
                actor_optimizer.step()
                discounted_actor_losses.append(loss)
        # actor.zero_grad()
        total_actor_loss = torch.cat(discounted_actor_losses).sum()
        # total_actor_loss.backward()
        # actor_optimizer.step()
        print(game.status())
        save_model(actor, 'actor')
        save_model(critic, 'critic')
        avg_actor_loss = total_actor_loss / max(1, len(discounted_actor_losses))
        avg_critic_loss = sum(critic_losses) / len(critic_losses)
        return avg_actor_loss, avg_critic_loss

    def train_on_memory(batch_size):
        losses = []
        for state, action_index, nextState, reward in random.sample(memory, min(batch_size, len(memory))):
            loss = update_critic(state, action_index, nextState, reward)
            losses.append(loss)
        return sum(losses) / max(1, len(losses))

    for epoch in range(num_epochs):
        avg_actor_loss, avg_critic_loss = run_episode()
        mem_loss = 'N/A'
        if mode in [ACTOR_CRITIC, Q_BASIC]:
            mem_loss = train_on_memory(batch_size)
        if True: #(epoch + 1) % max(1,(num_epochs // 10)) == 0:
            print('episode losses at epoch {}:\n\tactor: {}\n\tcritic: {}\n\tcritic batch: {}'.format(
                epoch+1, avg_actor_loss, avg_critic_loss, mem_loss))

    save_model(actor, 'actor')
    save_model(critic, 'critic')
    return actor, critic

if __name__ == '__main__':
    # train(12, 4, num_epochs=10, use_critic=True, exploration_rate=1)
    train(12, 4, num_epochs=200, mode=ACTOR_CRITIC, load=False, exploration_rate=0, discount_rate=.1)
