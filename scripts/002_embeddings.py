#!/usr/bin/env python3.7

from file_actions import generate_embeddings
from file_actions import save_tensors_as_NPZ
from dataset_processing import create_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

# A script that has to be run after embeddings were generated

data = create_data('data/002/')

"""
generate_embeddings('esm/extract.py', data['train']['FASTA'], data['train']['embeddings'])
generate_embeddings('esm/extract.py', data['validate']['FASTA'], data['validate']['embeddings'])
generate_embeddings('esm/extract.py', data['test']['FASTA'], data['test']['embeddings'])
"""

filter_sequences(data, 'train', data['train']['embeddings'])
filter_sequences(data, 'validate', data['validate']['embeddings'])
filter_sequences(data, 'test', data['test']['embeddings'])

[Xs_train_tensor, Ys_train_tensor] = get_ESM_embeddings_as_tensor(data, ['train'])
[Xs_validate_tensor, Ys_validate_tensor] = get_ESM_embeddings_as_tensor(data, ['validate'])
[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, ['test'])

save_tensors_as_NPZ([Xs_train_tensor, Ys_train_tensor, Xs_validate_tensor, Ys_validate_tensor], ['x_train', 'y_train', 'x_validate', 'y_validate'], 'data/002/NPZ/training_and_validation_embeddings.npz')
save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], ['x_test', 'y_test'], 'data/002/NPZ/testing_embeddings.npz')