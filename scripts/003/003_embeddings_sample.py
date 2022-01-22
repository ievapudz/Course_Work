#!/usr/bin/env python3.7

# A script that has to be run after embeddings were generated

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

data = create_data('data/003/', dataset_names=['training_v2', 
                                               'validation_v2',
                                               'testing_v2'])

filter_sequences(data, 'train', data['train']['embeddings'])
filter_sequences(data, 'validate', data['validate']['embeddings'])
filter_sequences(data, 'test', data['test']['embeddings'])

[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['train'])
[Xs_validate_tensor, Ys_validate_tensor] = get_ESM_embeddings_as_tensor(data, 
                                                                  ['validate'])
[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, ['test'])

save_tensors_as_NPZ([Xs_train_tensor, Ys_train_tensor, 
                     Xs_validate_tensor, Ys_validate_tensor], 
                    ['x_train', 'y_train', 'x_validate', 'y_validate'], 
                    'data/003/NPZ/training_and_validation_embeddings_sample.npz')

