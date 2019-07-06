import torch
from torch import nn
from torch.distributions import Categorical
from utils import *

class Actor(nn.Module):
    '''state -> action'''
    def __init__(self, state_size, num_actions, hidden_dims=120):
        super(Actor, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_size, hidden_dims),
            nn.ReLU(),
            nn.Dropout(.15),
            nn.Linear(hidden_dims, hidden_dims),
            nn.ReLU(),
            nn.Dropout(.15),
            nn.Linear(hidden_dims, num_actions),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, state):
        '''
        state (batch, width*height)
        returns action SM (batch, num_actions)
        '''
        return self.fc(state)
    
    def choose_action(self, state):
        '''
        state (batch, width*height)
        returns int for action
        '''
        sm = self.forward(state)
        dist = Categorical(sm)
        index = dist.sample()
        logprob = dist.log_prob(index)
        return logprob, index

class Critic(nn.Module):
    '''state, action -> reward'''
    def __init__(self, state_size, num_actions, hidden_dims=120):
        super(Critic, self).__init__()
        self.num_actions = num_actions

        self.fc = nn.Bilinear(state_size, num_actions, hidden_dims)
        self.activation = nn.ReLU()
        self.out = nn.Sequential(
            nn.Dropout(.15),
            nn.Linear(hidden_dims, hidden_dims),
            self.activation,
            nn.Dropout(.15),
            nn.Linear(hidden_dims, 1),
        )
    
    def forward(self, state, action):
        '''
        state (batch, width*height)
        action SM (batch, num_actions)
        returns reward scalar tensor
        '''
        # multi argument bilinear in sequential call may cause bug
        action = one_hot(action, self.num_actions)
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
