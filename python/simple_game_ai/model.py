import torch
from torch import nn

class Actor(nn.Module):
     '''state -> action'''
    def __init__(self, state_size, num_actions, hidden_dims=32):
        super(Actor, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_size, hidden_dims),
            nn.Tanh(),
            nn.Linear(hidden_dims, num_actions),
            nn.Softmax()
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
        confidence, index = torch.max(sm, dim=-1)
        return confidence, index

class Critic(nn.Module):
    '''state, action -> reward'''
    def __init__(self, state_size, num_actions, hidden_dims=32):
        super(Critic, self).__init__()
        self.fc = nn.Sequential(
            nn.Bilinear(state_size, num_actions, hidden_dims),
            nn.Tanh(),
            nn.Linear(hidden_dims, 1)
        )
    
    def forward(self, state, action):
        '''
        state (batch, width*height)
        action SM (batch, num_actions)
        returns reward scalar tensor
        '''
        # multi argument bilinear in sequential call may cause bug
        return self.fc(state, action)
