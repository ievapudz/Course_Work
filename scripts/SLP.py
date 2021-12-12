from torch import nn

class SLP(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.
    
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 1),
        )

    def forward(self, x):
        return self.layers(x)

class SLP_with_sigmoid(nn.Module):

    #This model requires BCELoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)