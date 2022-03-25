#!/usr/bin/env python3.7

# A script that filters out sequences that do not have embeddings
# and saves them to one FASTA file.

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

data = create_data('data/003/', dataset_names=['training_v2', 
                                               'validation_v2',
                                               'testing_v2'])

filter_sequences(data, 'train', data['train']['embeddings'])

filter_sequences(data, 'validate', data['validate']['embeddings'])

filter_sequences(data, 'test', data['test']['embeddings'])

for key in data.keys():
    for record in data[key]['X_filtered']:
        print('>'+record.name)
        print(record.seq)
