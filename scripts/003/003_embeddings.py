#!/usr/bin/env python3.7

# A script that saves training and validation embeddings to
# NPZ file.
# It has to be run after embeddings were generated.

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import generate_embeddings
from file_actions import save_tensors_as_NPZ
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

print("Converting ESM embeddings (training) to tensor")
[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['train'])
print("Converting ESM embeddings (validation) to tensor")
[Xs_validate_tensor, Ys_validate_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['validate'])
print("Saving tensors to NPZ file")
save_tensors_as_NPZ([Xs_train_tensor, Ys_train_tensor, 
                     Xs_validate_tensor, Ys_validate_tensor], 
                    ['x_train', 'y_train', 'x_validate', 'y_validate'], 
                    'data/003/NPZ/training_and_validation_embeddings_v2.npz')

