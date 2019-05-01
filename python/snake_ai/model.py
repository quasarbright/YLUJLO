import torch
from torch import nn
from torch.distributions import Categorical
from utils import *

class Q(nn.Module):
    '''state, action -> reward'''
    def __init__(self, state_size, num_actions, hidden_dims=64):
        super(Q, self).__init__()
        self.num_actions = num_actions

        self.fc = nn.Bilinear(state_size, num_actions, hidden_dims)
        self.activation = nn.Tanh()
        self.out = nn.Linear(hidden_dims, 1)
    
    def forward(self, state, action):
        '''
        state (batch, state_size)
        action (batch,) gets one-hotted
        returns reward scalar tensor
        '''
        # multi argument bilinear in sequential call may cause bug
        action = one_hot(action, self.num_actions) # now (batch, num_actions) one-hot
        fc = self.fc(state, action)
        activated = self.activation(fc)
        return self.out(activated)
    def choose_action(self, states):
        '''
        states (batch, state_size)
        output (batch,)
        '''
        batch_size, state_size = states.shape
        ans = torch.zeros((batch_size)).long().to(device)
        for i, state in enumerate(states):
            state = state.unsqueeze(0)
            best_action = 0
            best_value = float('-inf')
            for action in range(self.num_actions):
                value = self.forward(state, [action]).item()
                if value > best_value:
                    best_value = value
                    best_action = action
            ans[i] = best_action
        return ans

if __name__ == '__main__':
    # example usage
    q = Q(state_size=3, num_actions=2).to(device)
    state = torch.randn((1, 3)).to(device)
    action = [0]
    value = q(state, action)
    best_action = q.choose_action(state)
    best_value = q(state, q.choose_action(state))
    print(state, action, value, best_action, best_value, sep='\n')

