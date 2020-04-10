import time
from model import *
from utils import *
from game import VisibleGame
import p5

def run_model(q=False):
    actor = load_model('actor')
    actor.eval()
    critic = load_model('critic')
    critic.eval()

    def run_episode(show=True):
        '''
        play the game and remember what happened
        '''
        game = VisibleGame(10,10, run=False)
        # playing vars
        state = state_to_tensor(game.return_state())
        gameOver = False

        def draw():
            nonlocal show, game, gameOver, q, state, actor, critic
            if show:
                game.draw()
            # play an episode
            if gameOver:
                print('DEATH')
                print('DEATH')
                print('DEATH')
                p5.exit()
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
        p5.run(game.setup, draw, 144)
    run_episode()

if __name__ == '__main__':
    run_model(q=False)
