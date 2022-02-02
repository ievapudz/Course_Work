#!/usr/bin/env python3.7

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import print_tensor_as_CSV
from dataset_processing import create_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

print("Creating data object")
data = create_data('data/003/', dataset_names=['training_v2', 
                                               'validation_v2',
                                               'testing_v2'])                                                                                           

print("Filtering training data")
filter_sequences(data, 'train', data['train']['embeddings'])

print("Filtering validation data")
filter_sequences(data, 'validate', data['validate']['embeddings'])

print("Filtering testing data")
filter_sequences(data, 'validate', data['testing']['embeddings'])

print("Converting ESM embeddings (training) to tensor")
[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['train'])
print("Converting ESM embeddings (validation) to tensor")
[Xs_validate_tensor, Ys_validate_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['validate'])

print("Converting ESM embeddings (testing) to tensor")
[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['test'])

print_tensor_as_CSV(data, ['x_test', 'y_test'])