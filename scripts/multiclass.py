from torch import nn

class MultiClass1(nn.Module):

	# A model for multiclass (16) classification
	
	def __init__(self):
		super().__init__()
		self.layers = nn.Sequential(
			nn.Linear(1280, 16),
			nn.Softmax()
		)

	def forward(self, x):
		return self.layers(x)

