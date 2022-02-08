#!/usr/bin/env python3.7

# A script that saves testing embeddings to NPZ file.
# It has to be run after embeddings were generated.

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import generate_embeddings
from file_actions import save_tensors_as_NPZ
from dataset_processing import create_testing_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

print("Creating data object")
data = create_testing_data('data/003/', dataset_names=['testing_v2'])

print("Filtering testing data")
filter_sequences(data, 'test', data['test']['embeddings'])

print("Converting ESM embeddings (testing) to tensor")
[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, ['test'])

print("Saving tensors to NPZ file")
save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], ['x_test', 'y_test'], 
                    'data/003/NPZ/testing_embeddings_v2.npz')
