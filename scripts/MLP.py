from torch import nn

class MLP_2_2(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 2),
            nn.Sigmoid(),
            nn.Linear(2, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_4(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 4),
            nn.Sigmoid(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_8(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 8),
            nn.Sigmoid(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_16(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 16),
            nn.Sigmoid(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

