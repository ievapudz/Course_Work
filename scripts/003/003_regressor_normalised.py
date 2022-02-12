#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import normalise_labels
from regressor import Regressor
import torch
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torch import nn
from model_flow import train_epoch
from model_flow import validation_epoch

BATCH_SIZE = 24
EPOCH_BATCH_SIZE = 18
NUM_OF_EPOCHS = 4

dataset = load_tensor_from_NPZ(
    'data/003/NPZ/training_and_validation_embeddings_v2.npz', 
    ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)

normalise_labels(dataset, ['y_train', 'y_validate'], denominator=100)

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])  
validateloader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, 
                 shuffle=True)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the model
regressor = Regressor()

# Define the loss function (with activation function) and optimizer
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(regressor.parameters(), lr=1e-4)

for epoch in range(0, NUM_OF_EPOCHS):
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    
    train_epoch(regressor, trainloader, loss_function, optimizer, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, epoch)
    validation_epoch(regressor, validateloader, loss_function, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, NUM_OF_EPOCHS, epoch, '',
                '')

print('Training and validation process has finished.')
