import time
from model import *
from utils import *
from game import VisibleGame

def run_model(q=False):
    actor = load_model('actor')
    critic = load_model('critic')

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
                time.sleep(1/5)
            # play an episode
            if gameOver:
                print('DEATH')
                print('DEATH')
                print('DEATH')
                break
            if not q:
                action_logprob, action_index = actor.choose_action(state)
            else:
                action_index = critic.choose_action(state)
            # observe next state and collect reward
            reward, nextState, gameOver = game.move_player(action_index)
            # print(reward)
            nextState = state_to_tensor(nextState)
            # update state
            state = nextState
        game.close()
    run_episode()

if __name__ == '__main__':
    run_model(q=False)
