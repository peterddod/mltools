import torch
from torch import nn
import copy


class PathedLayer(nn.Module):
    def __init__(self, layer):
        super(PathedLayer, self).__init__()

        self.layer = layer
        self.pathSelector = copy.deepcopy(layer)

    def getPath(self, X):
        with torch.no_grad():
            path = torch.relu_(self.pathSelector(X))
            path[path != 0] = 1
        
        return path

    def forward(self, X):
        path = self.getPath(X)
        y = self.layer(X)
        y = torch.mul(y, path).requires_grad_(True)
        
        return y