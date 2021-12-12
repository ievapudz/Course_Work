#!/usr/bin/env python3.7

import numpy
from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import convert_labels_to_binary
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torch import nn

NUM_OF_BATCHES = 16

dataset = load_tensor_from_NPZ('data/NPZ/training_and_validation_embeddings.npz', ['x_train', 'y_train', 'x_validate', 'y_validate'])

residual = len(dataset['x_validate']) % NUM_OF_BATCHES

trim_dataset(dataset, ['x_validate', 'y_validate'], NUM_OF_BATCHES)

convert_labels_to_binary(dataset, ['y_train', 'y_validate'], [37, 80])

train_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
trainloader = DataLoader(train_dataset, batch_size=16, shuffle=True)

validate_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate'])  
validateloader = DataLoader(validate_dataset, batch_size=16, shuffle=True)

print(len(trainloader.dataset))
print(len(validateloader.dataset))