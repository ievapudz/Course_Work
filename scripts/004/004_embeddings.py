#!/usr/bin/env python3.7

# A script that saves training and validation embeddings to
# NPZ file.
# It has to be run after embeddings were generated.

# Example usage:
# ./scripts/004/004_embeddings.py data/004/

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import generate_embeddings
from file_actions import save_tensors_as_NPZ
from file_actions import print_tensors_as_SV_to_file
from dataset_processing import create_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

DIR = sys.argv[1]

print("Creating data object")
data = create_data(DIR, dataset_names=['train', 
									   'validate',
									   'test'])

print("Filtering training data")
filter_sequences(data, 'train', data['train']['embeddings'])

print("Filtering validation data")
filter_sequences(data, 'validate', data['validate']['embeddings'])

print("Filtering validation data")
filter_sequences(data, 'test', data['test']['embeddings'])

print("Converting ESM embeddings (training) to tensor")
[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, 
																  ['train'])
print("Converting ESM embeddings (validation) to tensor")
[Xs_validate_tensor, Ys_validate_tensor] = get_ESM_embeddings_as_tensor(data, 
																  ['validate'])
print("Converting ESM embeddings (validation) to tensor")
[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, 
																  ['test'])
print("Saving (training and validation) tensors to NPZ file")
save_tensors_as_NPZ([Xs_train_tensor, Ys_train_tensor, 
					 Xs_validate_tensor, Ys_validate_tensor], 
					['x_train', 'y_train', 'x_validate', 'y_validate'], 
					DIR+'NPZ/training_and_validation_embeddings.npz')

print("Saving (testing) tensors to NPZ file")
save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], 
					['x_test', 'y_test'], DIR+'NPZ/testing_embeddings.npz')

data_train_tensor = { 'x_train': Xs_train_tensor, 'y_train': Ys_train_tensor }

print("Saving training tensors to a TSV file")
print_tensors_as_SV_to_file(data, data_train_tensor, 'train', ['x_train', 'y_train'],
							out_file_name=DIR+'TSV/training_tensors.tsv', 
							sep="\t", labelled=True)

data_validate_tensor = { 'x_validate': Xs_validate_tensor, 'y_validate': Ys_validate_tensor }

print("Saving validation tensors to a TSV file")
print_tensors_as_SV_to_file(data, data_validate_tensor, 'validate', ['x_validate', 'y_validate'],
							out_file_name=DIR+'TSV/validation_tensors.tsv',
							sep="\t", labelled=True)

data_test_tensor = { 'x_test': Xs_test_tensor, 'y_test': Ys_test_tensor }

print("Saving testing tensors to a TSV file")
print_tensors_as_SV_to_file(data, data_test_tensor, 'test', ['x_test', 'y_test'],
							out_file_name=DIR+'TSV/testing_tensors.tsv',
							sep="\t", labelled=True)
