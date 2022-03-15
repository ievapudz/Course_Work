#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import torch
from optparse import OptionParser
from torch import nn
from model_dataset_processing import load_tensor_from_NPZ
from SLP import SLP_with_sigmoid
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from model_flow import unlabelled_test_epoch

parser = OptionParser()
parser.add_option("--npz", "-n", dest="npz",
                   help="path to the NPZ file")

parser.add_option("--output", "-o", dest="output",
                   help="output TSV file")

(options, args) = parser.parse_args()

PATH = './results/SLP/003/model.pt'

dataset = load_tensor_from_NPZ(options.npz, 
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
                      file_for_predictions=options.output,
                      binary_predictions_only=False)

print('Inference process has finished.')

