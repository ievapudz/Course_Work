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
from model_flow import unlabelled_test_epoch

PATH = './results/SLP/003/model.pt'

dataset = load_tensor_from_NPZ('data/CRISPR/NPZ/Cas12b_C_embeddings.npz', 
                               ['x_test', 'y_test'])

test_dataset = TensorDataset(dataset['x_test'], dataset['y_test'])  
test_loader = DataLoader(test_dataset, shuffle=False)

# Set fixed random number seed
torch.manual_seed(42)

# Load the trained SLP
model = SLP_with_sigmoid()
model.load_state_dict(torch.load(PATH))
model.eval()

print('Inference process begins')

unlabelled_test_epoch(model, test_loader, 0.5, 
                      file_for_predictions='results/SLP/CRISPR/Cas12b_C_predictions.tsv')

print('Inference process has finished.')

