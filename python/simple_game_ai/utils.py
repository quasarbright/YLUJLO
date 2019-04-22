import torch

device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

def state_to_tensor(state):
    t = torch.tensor(state).to(device).float()
    t = t.unsqueeze(0)
    return t

def one_hot(index_batch, length):
    t = torch.zeros(len(index_batch), length)
    for i, index in enumerate(index_batch):
        t[i,index] = 1
    return t.to(device)