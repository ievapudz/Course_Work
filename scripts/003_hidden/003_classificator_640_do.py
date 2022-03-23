#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import convert_labels_to_binary
from MLP import MLP_3_640_do
import torch
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torch import nn
from model_flow import train_epoch
from model_flow import validation_epoch

BATCH_SIZE = 24
EPOCH_BATCH_SIZE = 18
NUM_OF_EPOCHS = 15

DIR = './results/MLP_3_640_do/003/'
MODEL_PATH = DIR+'/model.pt'

# Create directories
command = 'mkdir '+DIR
os.system(command)
command = 'mkdir '+DIR+'ROC/ '+DIR+'confusion_matrices/'
os.system(command)

# Loading tensors
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
mlp_3_640_do = MLP_3_640_do()

# Define the loss function (with activation function) and optimizer
loss_function = nn.BCELoss()
optimizer = torch.optim.Adam(mlp_3_640_do.parameters(), lr=1e-4)

for epoch in range(0, NUM_OF_EPOCHS):
    # Print epoch
    print(f'Starting epoch {epoch+1}')
    
    train_epoch(mlp_3_640_do, trainloader, loss_function, optimizer, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, epoch)
    validation_epoch(mlp_3_640_do, validateloader, loss_function, BATCH_SIZE, 
                EPOCH_BATCH_SIZE, NUM_OF_EPOCHS, epoch, DIR+'/ROC/',
                DIR+'/confusion_matrices/')
  
print('Training and validation process has finished.')

torch.save(mlp_3_640_do.state_dict(), MODEL_PATH)