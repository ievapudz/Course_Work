#!/usr/bin/env python3.7

# A script that joins Cas12b embeddings together and newly edited 
# embeddings are saved to new NPZ and TSV files.

# It has to be run after embeddings were generated.

# Usage:
# ./scripts/CRISPR/Cas12b_embeddings.py > data/CRISPR/Cas12b_embeddings.tsv

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import print_joined_tensor_as_CSV
from file_actions import save_tensors_as_NPZ
from dataset_processing import create_testing_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor
from dataset_processing import join_embeddings

data_N = create_testing_data('data/CRISPR/', dataset_parent_dir=['Cas12b'],
                           dataset_names=['Cas12b_N'], labelled=False)

data_C = create_testing_data('data/CRISPR/', dataset_parent_dir=['Cas12b'],
                           dataset_names=['Cas12b_C'], labelled=False)

filter_sequences(data_N, 'test', data_N['test']['embeddings'], labelled=False)
filter_sequences(data_C, 'test', data_C['test']['embeddings'], labelled=False)

[Xs_N, Ys_N] = get_ESM_embeddings_as_tensor(data_N, ['test'])
[Xs_C, Ys_C] = get_ESM_embeddings_as_tensor(data_C, ['test'])

[Xs_test_tensor, Ys_test_tensor] = join_embeddings([data_N, data_C], ['test'])

save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], ['x_test', 'y_test'], 
                    'data/CRISPR/NPZ/Cas12b_embeddings.npz')

data_tensor = { 'x_test': Xs_test_tensor, 'y_test': Ys_test_tensor }

print_joined_tensor_as_CSV([data_N, data_C], data_tensor, 'test', ['x_test', 'y_test'], sep="\t", 
                    labelled=False)
