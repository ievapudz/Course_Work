#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import convert_labels_to_binary
from SLP import SLP
from SLP import SLP_with_sigmoid
import torch
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torch import nn
from model_flow import train_epoch
from model_flow import validation_epoch
from model_flow import test_epoch
from file_actions import print_tensor_elements

BATCH_SIZE = 24
EPOCH_BATCH_SIZE = 18
NUM_OF_EPOCHS = 5

dataset = load_tensor_from_NPZ(
    'data/003/NPZ/training_and_validation_embeddings_v2.npz', 
    ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)
convert_labels_to_binary(dataset, ['y_train', 'y_validate'])

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])  
validateloader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, 
                 shuffle=True)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the SLP
slp = SLP_with_sigmoid()

# Define the loss function (with activation function) and optimizer
loss_function = nn.BCELoss()
optimizer = torch.optim.Adam(slp.parameters(), lr=1e-4)

for epoch in range(0, NUM_OF_EPOCHS):
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    
    train_epoch(slp, trainloader, loss_function, optimizer, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, epoch)
    validation_epoch(slp, validateloader, loss_function, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, NUM_OF_EPOCHS, epoch, 
                ROC_curve_plot_file_dir='./results/SLP/003/ROC/',
                confusion_matrix_file_dir='./results/SLP/003/confusion_matrices/')

print('Training and validation process has finished.')

print('Testing process begins')

dataset_test_initial = load_tensor_from_NPZ(
    'data/003/NPZ/testing_embeddings_v2.npz',
    ['x_test', 'y_test'])

trim_dataset(dataset_test_initial, ['x_test', 'y_test'], BATCH_SIZE)

# Save the current dataset values to file
print_tensor_elements(dataset_test_initial, ['y_test'], 'data/003/temperature_predictions_correlation_x.lst')

convert_labels_to_binary(dataset_test_initial, ['y_test'])
  
test_dataset = TensorDataset(dataset_test_initial['x_test'], 
                             dataset_test_initial['y_test'])
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

test_epoch(slp, trainloader, loss_function, optimizer, BATCH_SIZE,
           EPOCH_BATCH_SIZE, 
           ROC_curve_plot_file_dir='./results/SLP/003/ROC/',
           confusion_matrix_file_dir='./results/SLP/003/confusion_matrices/', 
           file_for_predictions='data/003/temperature_predictions_correlation_y.lst')

print('Testing process has finished.')

