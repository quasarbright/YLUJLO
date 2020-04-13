import random
from model import *
from game import *
from utils import *



def train(state_size, num_actions, discount_rate=.9, exploration_rate=.5, lr=.005, num_epochs=10, mode=REINFORCE, batch_size=100, load=False):
    print(locals())
    # if (exploration_rate != 0) and (mode in [REINFORCE, ACTOR_CRITIC]):
    #     print("================WARNING================")
    #     print("using non-zero exploration with a reinforce agent is weird")
    # desired behavior: by the last epoch, exploration rate = final exploration rate
    # e_t = e_0 * r ^ (t - 1)
    # e_E = e_f => r = (e_f / e_0) ^ (1 / (E-1))
    # where E = num_epochs
    # r = expl_factor
    # agent and environment
    actor = Actor(state_size, num_actions).to(device)
    actor_optimizer = torch.optim.Adam(actor.parameters(), lr=lr/10)
    critic = Critic(state_size, num_actions).to(device)
    critic_loss = nn.MSELoss()
    critic_optimizer = torch.optim.Adam(critic.parameters(), lr=lr)
    if load:
        actor = load_model('actor_{}'.format(mode))
        critic = load_model('critic_{}'.format(mode))
    
    memory = [] # [(state, action index, next state, reward), ...]

    def batch_action(action):
        return torch.tensor([action]).long().to(device)

    def update_critic(state, action_index, nextState, reward):
        value = critic(state, action_index)

        # find best next move according to critic
        max_next_value = critic(nextState, batch_action(0))
        for next_action in range(1, num_actions):
            next_action = batch_action(next_action)
            next_value = critic(nextState, next_action)
            if next_value > max_next_value:
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
        nonlocal exploration_rate
        game = Game(10,10)
        # playing vars
        state = state_to_tensor(game.return_state())
        reward = 0
        gameOver = False

        critic_losses = []
        actor_losses = []

        action_logprobs = []
        rewards = [] # only rewards from the actor's moves
        qs = [] # predicted rewards from the critic
        for _ in range(200):
            if show:
                print()
                print(game)
            # play an episode
            if gameOver:
                break
            should_explore = random.random() < exploration_rate
            if mode in [REINFORCE, ACTOR_CRITIC]:
                action_logprob, action_index = actor.choose_action(state)
            elif mode == Q_BASIC:
                action_index = critic.choose_action(state)
            if should_explore and mode == Q_BASIC:
                # sometimes, do a random action just to see what happens
                action_logprob, action_index = torch.tensor(1 / num_actions).to(device), batch_action(random.randint(0, num_actions-1))
            # observe next state and collect reward
            reward, nextState, gameOver = game.move_player(action_index)
            nextState = state_to_tensor(nextState)
            q = critic(state, action_index)

            if mode == ACTOR_CRITIC:
                score = q * action_logprob
                loss = -score
                loss.backward()
                actor_optimizer.step()
                actor_losses.append(loss)
            
            critic_loss = update_critic(state, action_index, nextState, reward)
            critic_losses.append(critic_loss)

            if (not should_explore) or mode in [REINFORCE, ACTOR_CRITIC]:
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
        R = 0
        if mode == REINFORCE:
            for reward in rewards[::-1]:
                R = reward + discount_rate * R
                values.insert(0,R)
            for logprob, value in zip(action_logprobs, values):
                actor.zero_grad()
                score = logprob * value
                loss = -score
                loss.backward()
                actor_optimizer.step()
                actor_losses.append(loss)
        # actor.zero_grad()
        if len(actor_losses) != 0:
            total_actor_loss = torch.cat(actor_losses).sum()
        else:
            total_actor_loss = 0
        # total_actor_loss.backward()
        # actor_optimizer.step()
        print(game.status())
        save_model(actor, 'actor_{}'.format(mode))
        save_model(critic, 'critic_{}'.format(mode))
        avg_actor_loss = total_actor_loss / max(1, len(actor_losses))
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
            print('episode losses at epoch {}:\n\tactor: {}\n\tcritic: {}\n\tcritic on memories: {}'.format(
                epoch+1, avg_actor_loss, avg_critic_loss, mem_loss))

    save_model(actor, 'actor_{}'.format(mode))
    save_model(critic, 'critic_{}'.format(mode))
    return actor, critic

if __name__ == '__main__':
    # train(12, 4, num_epochs=10, use_critic=True, exploration_rate=1)
    train(12, 4, num_epochs=200, exploration_rate=.5, mode=Q_BASIC, load=False, discount_rate=.1, batch_size=250)
