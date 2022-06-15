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

dataset = load_tensor_from_NPZ('data/003/NPZ/testing_embeddings_v2.npz', 
							   ['x_test', 'y_test'])

convert_labels_to_binary(dataset, ['y_test'])

test_tensor_dataset = TensorDataset(dataset['x_test'], dataset['y_test'])  
test_loader = DataLoader(test_tensor_dataset, shuffle=False)

# Set fixed random number seed
torch.manual_seed(42)

# Load the trained SLP
model = SLP_with_sigmoid()
model.load_state_dict(torch.load(PATH))
model.eval()

print('Inference process begins')

test_epoch(model, test_loader, BATCH_SIZE, prefix='testing_inference_', 
		   ROC_curve_plot_file_dir='./results/SLP/003/ROC/',
			   confusion_matrix_file_dir='./results/SLP/003/confusion_matrices/',
			   file_for_predictions='results/SLP/003/testing_predictions.tsv', print_true_labels=True)

print('Inference process has finished.')

