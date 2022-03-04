#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import normalise_labels_as_z_scores
from regressor import Regressor
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
NUM_OF_EPOCHS = 4

dataset = load_tensor_from_NPZ(
    'data/003/NPZ/training_and_validation_embeddings_v2.npz', 
    ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)

normalise_labels_as_z_scores(dataset, ['y_train', 'y_validate'], ref_point=65)

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])  
validateloader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, 
                 shuffle=False)

# Set fixed random number seed
torch.manual_seed(42)

# Initialize the model
regressor = Regressor()

# Define the loss function (with activation function) and optimizer
loss_function = nn.MSELoss()
optimizer = torch.optim.Adam(regressor.parameters(), lr=1e-4)

for epoch in range(0, NUM_OF_EPOCHS):
    train_epoch(regressor, trainloader, loss_function, optimizer, BATCH_SIZE,
                EPOCH_BATCH_SIZE, epoch, print_loss=False)
    validation_epoch(regressor, validateloader, loss_function, BATCH_SIZE,
                EPOCH_BATCH_SIZE, NUM_OF_EPOCHS, epoch, '',
                '', print_loss=False, print_predictions=False)

dataset_test_initial = load_tensor_from_NPZ(
    'data/003/NPZ/testing_embeddings_v2.npz',
    ['x_test', 'y_test'])

trim_dataset(dataset_test_initial, ['x_test', 'y_test'], BATCH_SIZE)

normalise_labels_as_z_scores(dataset_test_initial, ['y_test'], ref_point=65)

test_dataset = TensorDataset(dataset_test_initial['x_test'],
                             dataset_test_initial['y_test'])
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

test_epoch(regressor, test_loader, BATCH_SIZE, prefix='',
           ROC_curve_plot_file_dir='',
           confusion_matrix_file_dir='', 
           file_for_predictions='results/regressor/003/testing_4_real_and_predictions_normalised.tsv')


