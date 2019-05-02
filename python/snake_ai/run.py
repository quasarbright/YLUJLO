import time
from model import *
from utils import *
from game import VisibleGame

def run_model(num_episodes=1, perfect=False):
    q = load_model('q')

    def run_episode(show=True):
        '''
        play the game and remember what happened
        '''
        game = VisibleGame(10,10)
        # playing vars
        state = state_to_tensor(game.return_state())
        gameOver = False

        for t in range(1000):
            if show:
                game.draw()
                time.sleep(1/100)
            # play an episode
            if gameOver:
                print('DEATH')
                print('DEATH')
                print('DEATH')
                break
            if perfect:
                action_index = game.best_move()
            else:
                action_index = q.choose_action(state)
            # observe next state and collect reward
            reward, nextState, gameOver = game.move_player(action_index)
            print(reward, action_index)
            nextState = state_to_tensor(nextState)
            # update state
            state = nextState
        game.close()
    for _ in range(num_episodes):
        run_episode()

if __name__ == '__main__':
    run_model(perfect=False)
