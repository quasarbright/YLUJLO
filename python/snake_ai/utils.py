import torch
import torch.utils.data

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'


def batch_action(action):
    return torch.tensor([action]).long().to(device)

def state_to_tensor(state):
    t = torch.tensor(state).to(device).float()
    t = t.unsqueeze(0)
    return t

def one_hot(index_batch, length):
    '''
    index_batch array-like (batch,)
    '''
    t = torch.zeros(len(index_batch), length).to(device)
    for i, index in enumerate(index_batch):
        t[i,index] = 1
    return t

def memory_dataloader(memory, batch_size):
    states = []
    actions = []
    nextStates = []
    rewards = []
    for experience in memory:
        state, action, nextState, reward = experience
        states.append(state)
        actions.append(action)
        nextStates.append(nextState)
        rewards.append(torch.tensor([reward]).to(device))
    states = torch.cat(states)
    actions = torch.stack(actions)
    nextStates = torch.cat(nextStates)
    rewards = torch.stack(rewards).float()

    dataset = torch.utils.data.TensorDataset(states, actions, nextStates, rewards)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader

def path(name):
    return 'saves/{}.pt'.format(name)

def save_model(model, name):
    torch.save(model, path(name))

def load_model(name):
    model = torch.load(path(name))
    model.eval()
    return model
