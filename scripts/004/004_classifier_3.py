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
from model_dataset_processing import convert_labels_to_temperature_class
from multiclass import MultiClass3
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from model_flow import train_epoch_multiclass
from model_flow import validation_epoch_multiclass

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

(options, args) = parser.parse_args()

PATH = './results/MultiClass3/004/model.pt'

if(options.model != None):
	PATH = options.model

BATCH_SIZE = int(options.batch_size)
NUM_OF_EPOCHS = int(options.epochs)

dataset = load_tensor_from_NPZ(options.npz, 
							   ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)

convert_labels_to_temperature_class(dataset, ['y_train', 'y_validate'])

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])
validate_loader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the SLP
model = MultiClass3()

# Define the loss function (with activation function) and optimizer
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=float(options.learning_rate))

for epoch in range(0, NUM_OF_EPOCHS):
	# Print epoch
	print(f'Starting epoch {epoch+1}')

	train_epoch_multiclass(model, train_loader, loss_function, optimizer, BATCH_SIZE)
	validation_epoch_multiclass(model, validate_loader, loss_function, BATCH_SIZE,
				NUM_OF_EPOCHS, epoch, '',
				'')

print('Training and validation process has finished.')

torch.save(model.state_dict(), PATH)
