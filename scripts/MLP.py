from torch import nn

class MLP_2_2(nn.Module):

    #This model requires BCEWithLogitsLoss function to be used in the model's flow.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 2),
            nn.ReLU(),
            nn.Linear(2, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_4(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_8(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_16(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_2_640(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 640),
            nn.ReLU(),
            nn.Linear(640, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_3_640_bn1(nn.Module):

    # A model with batch normalisation included.

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 640),
            nn.BatchNorm1d(640, affine=False),
            nn.ReLU(),
            nn.Linear(640, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)

class MLP_3_640_do(nn.Module):

    # A model with a dropout layer included
    # before the hidden layer..

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(1280, 640),
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(640, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)
