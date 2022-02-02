#!/usr/bin/env python3.7

# A script to write training tensors to a CSV file
# Usage: ./scripts/003/003_convert_NPZ_to_CSV_training.py > data/003/CSV/training_v2.csv

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import print_tensor_as_CSV
from dataset_processing import create_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

data = create_data('data/003/', dataset_names=['training_v2', 
                                               'validation_v2',
                                               'testing_v2'])                                                                                           

filter_sequences(data, 'train', data['train']['embeddings'])

[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['train'])

data_tensor = { 'x_training': Xs_train_tensor, 'y_train': Ys_train_tensor }
print_tensor_as_CSV(data, data_tensor, 'train', ['x_train', 'y_train'])
