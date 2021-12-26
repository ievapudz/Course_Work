#!/usr/bin/env python3.7

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

BATCH_SIZE = 8
EPOCH_BATCH_SIZE = 24
NUM_OF_EPOCHS = 51

dataset = load_tensor_from_NPZ('data/002/NPZ/training_and_validation_embeddings.npz', ['x_train', 'y_train', 'x_validate', 'y_validate'])

trim_dataset(dataset, ['x_train', 'y_train'], BATCH_SIZE)
trim_dataset(dataset, ['x_validate', 'y_validate'], BATCH_SIZE)
convert_labels_to_binary(dataset, ['y_train', 'y_validate'])

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])  
validateloader = DataLoader(validate_dataset, batch_size=BATCH_SIZE, shuffle=True)

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
    
    train_epoch(slp, trainloader, loss_function, optimizer, BATCH_SIZE, EPOCH_BATCH_SIZE, epoch)
    validation_epoch(slp, validateloader, loss_function, BATCH_SIZE, EPOCH_BATCH_SIZE, 
                    epoch, './results/SLP/002/ROC/', './results/SLP/002/confusion_matrices/')
  
print('Training and validation process has finished.')
