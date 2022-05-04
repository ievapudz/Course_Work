from torch import nn

class Regressor(nn.Module):

	# This is a regressor model to predict the
	# temperature of the organism that the protein
	# belongs to. 
	# The input of the model is protein's embedding
	# of 1280 dimensions.

	def __init__(self):
		super().__init__()
		self.layers = nn.Sequential(
			nn.Linear(1280, 1),
		)

	def forward(self, x):
		return self.layers(x)
