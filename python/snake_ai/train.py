import random
from model import *
from game import *
from utils import *

def train(state_size, num_actions, exploration_rate=.1, discount_rate=.9, lr=.1, num_episodes=10, num_epochs=500, batch_size=500):
    # agent and environment
    q = Q(state_size, num_actions).to(device)
    loss_fn = nn.MSELoss()
    optimizer = torch.optim.SGD(q.parameters(), lr=lr)
    
    memory = [] # [(state, action index, next state, reward), ...]

    def update(state, action_index, nextState, reward):
        value = q(state, action_index)

        # find best next move according to critic
        max_next_action = q.choose_action(nextState)
        max_next_value = q(nextState, max_next_action)
        # update q
        q.zero_grad()
        truth = max_next_value * discount_rate + reward
        loss = loss_fn(value, truth)
        loss.backward()
        optimizer.step()
        return loss

    def run_episode():
        '''
        play the game and remember what happened
        '''
        game = Game(20,20)
        # playing vars
        state = state_to_tensor(game.return_state())
        reward = 0
        gameOver = False

        losses = []

        for t in range(100):
            # play an episode
            if gameOver:
                break
            should_explore = random.random() < exploration_rate
            if should_explore:
                action = random.randint(0, num_actions-1) # python int
                action = batch_action(action) # shape (1,) torch long tensor
            else:
                action = q.choose_action(state) # shape (1,)
            reward, nextState, gameOver = game.move_player(action)
            nextState = state_to_tensor(nextState)
            experience = (state, action, nextState, reward)
            loss = update(*experience)
            losses.append(loss)
            memory.append(experience)
            # update state
            state = nextState
        avg_loss = sum(losses) / max(1, len(losses))
        return avg_loss

    def train_on_memory(batch_size):
        '''train on a single random batch'''
        losses = []
        for state, action_index, nextState, reward in random.sample(memory, min(batch_size, len(memory))):
            loss = update(state, action_index, nextState, reward)
            loss = loss.item()
            losses.append(loss)
        return sum(losses) / max(1, len(losses))

    print('training on episodes')
    for epoch in range(num_episodes):
        episode_loss = run_episode()
        mem_loss = train_on_memory(batch_size)
        if (epoch + 1) % max(1,(num_episodes // 10)) == 0:
            print('losses at epoch {}:\n\tepisode: {}\n\tmemory: {}'.format(epoch+1, episode_loss, mem_loss))
    print('training on all memory')
    
    dataloader = memory_dataloader(memory, batch_size)
    for epoch in range(num_epochs):
        losses = []
        for experience in dataloader:
            state, action, nextState, reward = experience
            loss = update(*experience)
            loss = loss.item()
            losses.append(loss)
        avg_loss = sum(losses) / max(1, len(losses))
        if (epoch+1) % (num_epochs // 10) == 0:
            print('loss at epoch {}: {}'.format(epoch+1, avg_loss))


    save_model(q, 'q')
    return q

if __name__ == '__main__':
    train(6, 5, num_episodes=100, batch_size=50, num_epochs=100)
