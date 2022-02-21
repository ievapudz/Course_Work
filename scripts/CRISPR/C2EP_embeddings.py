#!/usr/bin/env python3.7

# A script that saves CRISPR sequences embeddings to
# NPZ file.
# It has to be run after embeddings were generated.

# Usage:
# ./scripts/CRISPR/C2EP_embeddings.py > data/CRISPR/C2EP_embeddings.tsv

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import print_tensor_as_CSV
from file_actions import save_tensors_as_NPZ
from dataset_processing import create_testing_data
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

data = create_testing_data('data/CRISPR/', dataset_names=['C2EP'], 
                           dataset_parent_dir=['C2EP'], labelled=False)

filter_sequences(data, 'test', data['test']['embeddings'], labelled=False)

[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, ['test'])

save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], ['x_test', 'y_test'], 
                    'data/CRISPR/NPZ/C2EP_embeddings.npz')

data_tensor = { 'x_test': Xs_test_tensor, 'y_test': Ys_test_tensor }

print_tensor_as_CSV(data, data_tensor, 'test', ['x_test', 'y_test'], sep="\t", 
                    labelled=False)
