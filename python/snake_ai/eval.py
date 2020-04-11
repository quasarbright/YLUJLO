from utils import *
from model import *
from game import Game

def eval(mode, num_episodes):
    actor = load_model('actor')
    actor.eval()
    critic = load_model('critic')
    critic.eval()

    def run_episode():
        game = Game(10,10)
        # playing vars
        gameOver = False
        state = game.return_state()
        for t in range(1000):
            if gameOver:
                break
            state_ = state_to_tensor(state)
            # play an episode
            if mode in [REINFORCE, ACTOR_CRITIC]:
                _, action_index = actor.choose_action(state_)
            else:
                action_index = critic.choose_action(state_)
            # observe next state and collect reward
            _, state, gameOver = game.move_player(action_index)
        return game.status()
    ages = []
    scores = []
    for _ in range(num_episodes):
        status = run_episode()
        ages.append(status["age"])
        scores.append(status["score"])
    avg_age = sum(ages) / max(1, len(ages))
    avg_scores = sum(scores) / max(1, len(scores))
    return {"avg_age": avg_age, "avg_score":avg_scores}

if __name__ == '__main__':
    print(eval(Q_BASIC, 50))