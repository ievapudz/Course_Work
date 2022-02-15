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

PATH = './results/SLP/003/model.pt'

dataset = load_tensor_from_NPZ(
    'data/CRISPR/NPZ/C2EP.npz', 
    ['x_test', 'y_test'])

trim_dataset(dataset, ['x_test', 'y_test'], BATCH_SIZE)
convert_labels_to_binary(dataset, ['y_test'])

test_dataset = TensorDataset(dataset['x_test'], dataset['y_test'])  
testloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the SLP
slp = torch.load(PATH)

# Define the loss function (with activation function) and optimizer
loss_function = nn.BCELoss()
optimizer = torch.optim.Adam(slp.parameters(), lr=1e-4)

print('Testing process begins')

convert_labels_to_binary(test_dataset, ['y_test'])
  
test_dataset = TensorDataset(dataset_test_initial['x_test'], 
                             dataset_test_initial['y_test'])
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

test_epoch(slp, test_loader, loss_function, optimizer, BATCH_SIZE,
           EPOCH_BATCH_SIZE, 
           ROC_curve_plot_file_dir='./results/SLP/CRISPR/ROC/',
           confusion_matrix_file_dir='./results/SLP/CRISPR/confusion_matrices/', 
           file_for_predictions='data/CRISPR/predictions.tsv')

print('Testing process has finished.')

