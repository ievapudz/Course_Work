from torch import nn

class MultiClass1(nn.Module):

	# A model for multiclass (16) classification
	
	def __init__(self):
		super().__init__()
		self.layers = nn.Sequential(
			nn.Linear(1280, 16),
			nn.Softmax(dim=1)
		)

	def forward(self, x):
		return self.layers(x)

class MultiClass2(nn.Module):

	# A model for multi-class (16) classification

	def __init__(self):
		super().__init__()
		self.layers = nn.Sequential(
			nn.Linear(1280, 640),
			nn.ReLU(),
			nn.Linear(640, 16),
			nn.Softmax(dim=1)
		)

	def forward(self, x):
		return self.layers(x)

class MultiClass3(nn.Module):

	# A model for multi-class (16) classification

	def __init__(self):
		super().__init__()
		self.layers = nn.Sequential(
			nn.Linear(1280, 640),
			nn.ReLU(),
			nn.Linear(640, 320),
			nn.ReLU(),
			nn.Linear(320, 16),
			nn.Softmax(dim=1)
		)

	def forward(self, x):
		return self.layers(x)
