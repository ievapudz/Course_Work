#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import torch
from optparse import OptionParser
from torch import nn
from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import normalise_labels_as_z_scores
from regressor import Regressor
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from model_flow import train_epoch
from model_flow import validation_epoch

parser = OptionParser()
parser.add_option("--npz", "-n", dest="npz",
				   help="path to the NPZ file")

parser.add_option("--batch", "-b", dest="batch_size",
				   default=24, help="batch size")

parser.add_option("--learning_rate", "-l", dest="learning_rate",
				   default=1e-4, help="learning rate")

parser.add_option("--epochs", "-e", dest="epochs",
				   default=5, help="number of epochs")

parser.add_option("--model", "-m", dest="model",
				   default=None, help="model file")

parser.add_option("--ROC_dir", "-r", dest="ROC_dir",
				   help="directory with ROC curves")

parser.add_option("--output", "-o", dest="output",
				   help="output TSV file")

parser.add_option("--predictions", "-p", dest="predictions",
				   default=None, help="TSV file with predictions")

(options, args) = parser.parse_args()

PATH = './results/regressor/004/model.pt'

if(options.model != None):
	PATH = options.model

BATCH_SIZE = int(options.batch_size)
NUM_OF_EPOCHS = int(options.epochs)

dataset = load_tensor_from_NPZ(options.npz, 
							   ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)

normalise_labels_as_z_scores(dataset, ['y_train', 'y_validate'], ref_point=65)

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])
validate_loader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the model
model = Regressor()

# Define the loss function (with activation function) and optimizer
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=float(options.learning_rate))

for epoch in range(0, NUM_OF_EPOCHS):
	train_epoch(model, train_loader, loss_function, optimizer, BATCH_SIZE,
				print_predictions=False, print_loss=True)

	if(options.predictions):
		validation_epoch(model, validate_loader, loss_function, BATCH_SIZE,
					 NUM_OF_EPOCHS, epoch,
					 ROC_curve_plot_file_dir='',
					 confusion_matrix_file_dir='',
					 print_predictions=True, print_loss=True)
	else:
		validation_epoch(model, validate_loader, loss_function, BATCH_SIZE,
					 NUM_OF_EPOCHS, epoch,
					 ROC_curve_plot_file_dir='',
					 confusion_matrix_file_dir='',
					 print_predictions=False, print_loss=True)

print('Training and validation process has finished.')

torch.save(model.state_dict(), PATH)
