import random
from model import *
from game import *
from utils import *

def train(state_size, num_actions, exploration_rate=.1, discount_rate=.9, lr=.005, num_epochs=10, use_critic=True, batch_size=500, load=False):
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

        for t in range(200):
            if show:
                print()
                print(game)
            # play an episode
            if gameOver:
                break
            action_logprob, action_index = actor.choose_action(state)
            should_explore = random.random() < exploration_rate
            if should_explore:
                # sometimes, do a random action just to see what happens
                action_logprob, action_index = torch.tensor(1 / num_actions).to(device), batch_action(random.randint(0, num_actions-1))
            # observe next state and collect reward
            reward, nextState, gameOver = game.move_player(action_index)
            nextState = state_to_tensor(nextState)
            value = critic(state, action_index)
            
            critic_loss = update_critic(state, action_index, nextState, reward)
            critic_losses.append(critic_loss)

            if not should_explore:
                # backprop rewards to actor
                actor.zero_grad()
                logprob = action_logprob
                if use_critic:
                    score = logprob * value
                else:
                    score = logprob * reward
                loss = -score
                # if reward >= 1:
                #     print(state)
                #     print(reward, action_index.item(), loss.item(), logprob.item(), value.item())
                actor_losses.append(loss.item())
                loss.backward()
                actor_optimizer.step()
            # remember what just happened
            memory.append((state, action_index, nextState, reward))
            # update state
            state = nextState
        print(game.status())
        save_model(actor, 'actor')
        save_model(critic, 'critic')
        avg_actor_loss = sum(actor_losses) / max(1, len(actor_losses))
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
        if use_critic:
            mem_loss = train_on_memory(batch_size)
        if True: #(epoch + 1) % max(1,(num_epochs // 10)) == 0:
            print('episode losses at epoch {}:\n\tactor: {}\n\tcritic: {}\n\tcritic batch: {}'.format(
                epoch+1, avg_actor_loss, avg_critic_loss, mem_loss))

    save_model(actor, 'actor')
    save_model(critic, 'critic')
    return actor, critic

if __name__ == '__main__':
    # train(12, 4, num_epochs=10, use_critic=True, exploration_rate=1)
    train(12, 4, num_epochs=500, use_critic=False, load=False, exploration_rate=0)
