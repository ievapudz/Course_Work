#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import torch
from torch import nn
from model_dataset_processing import load_tensor_from_NPZ
from SLP import SLP_with_sigmoid
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from model_flow import test_epoch
from model_dataset_processing import convert_labels_to_binary

PATH = './results/SLP/003/model.pt'
BATCH_SIZE = 24

dataset = load_tensor_from_NPZ('data/003/NPZ/training_and_validation_embeddings_v2.npz', 
                               ['x_train', 'y_train', 'x_validate', 'y_validate'])

convert_labels_to_binary(dataset, ['y_train', 'y_validate'])

train_tensor_dataset = TensorDataset(dataset['x_train'], dataset['y_train'])  
train_loader = DataLoader(train_tensor_dataset, shuffle=False)
validate_tensor_dataset = TensorDataset(dataset['x_validate'], dataset['y_validate']) 
validate_loader = DataLoader(validate_tensor_dataset, shuffle=False)

# Set fixed random number seed
torch.manual_seed(42)

# Load the trained SLP
model = SLP_with_sigmoid()
model.load_state_dict(torch.load(PATH))
model.eval()

print('Inference process begins')

test_epoch(model, train_loader, BATCH_SIZE, prefix='training_inference_', 
           ROC_curve_plot_file_dir='./results/SLP/003/ROC/',
               confusion_matrix_file_dir='./results/SLP/003/confusion_matrices/',
               file_for_predictions='results/SLP/003/training_predictions.tsv', print_true_labels=True)

test_epoch(model, validate_loader, BATCH_SIZE, prefix='validation_inference_', 
          ROC_curve_plot_file_dir='./results/SLP/003/ROC/',
          confusion_matrix_file_dir='./results/SLP/003/confusion_matrices/',
          file_for_predictions='results/SLP/003/validation_predictions.tsv', print_true_labels=True)

print('Inference process has finished.')

