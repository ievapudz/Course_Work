#!/usr/bin/env python3.7

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import trim_dataset
from model_dataset_processing import normalise_labels_as_z_scores
from model_dataset_processing import standard_deviation
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
MODEL = sys.argv[1]

# Initialize the model
model = Regressor()
model.load_state_dict(torch.load(MODEL))
model.eval()

dataset_test_initial = load_tensor_from_NPZ(
    'data/004/NPZ/testing_embeddings.npz',
    ['x_test', 'y_test'])

normalise_labels_as_z_scores(dataset_test_initial, ['y_test'], ref_point=65)

test_dataset = TensorDataset(dataset_test_initial['x_test'],
                             dataset_test_initial['y_test'])
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

predictions_out_file_tmp = 'results/regressor/004/testing_predictions.tmp'
predictions_out_file_tsv = 'results/regressor/004/testing_predictions.tsv'

test_epoch(model, test_loader, BATCH_SIZE,
           ROC_curve_plot_file_dir='',
           confusion_matrix_file_dir='', 
           file_for_predictions=predictions_out_file_tmp)

command = 'sed \'1 i temperature\tprediction\' '+predictions_out_file_tmp+' > '+predictions_out_file_tsv
os.system(command)
command = 'rm '+predictions_out_file_tmp
os.system(command)
