#!/usr/bin/env python3.7

from file_actions import generate_embeddings
from dataset_processing import create_data
from dataset_processing import filter_sequences

# A script that has to be run after embeddings were generated

data = create_data('data/002/')

generate_embeddings('esm/extract.py', data['validate']['FASTA'], data['validate']['embeddings'])

filter_sequences(data, 'train', data['train']['embeddings'])
filter_sequences(data, 'validate', data['validate']['embeddings'])
filter_sequences(data, 'test', data['test']['embeddings'])