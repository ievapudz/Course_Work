#!/usr/bin/env python3.7

import os
from Bio import SeqIO
from sklearn.utils import shuffle
from file_actions import write_to_file
from dataset_processing import filter_sequences
from visualise_embeddings import visualise_PCA_species
from visualise_embeddings import visualise_MDE_species
from file_actions import parse_proteomes
from file_actions import generate_embeddings

data = {
    '003': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000798', 'UP000008183', 'UP000001974_273057'],
        'temperature_labels': [80, 80, 80],
        'FASTA': 'data/cluster_tests/003/FASTA/003.fasta',
        'embeddings': 'data/cluster_tests/003/EMB_ESM1b/'
    },
    '004': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000625_83333', 'UP000077428', 'UP000000792'],
        'temperature_labels': [37, 37, 37],
        'FASTA': 'data/cluster_tests/004/FASTA/004.fasta',
        'embeddings': 'data/cluster_tests/004/EMB_ESM1b/'
    }
}

proteome_files_dir = 'data/proteomes/'
visualisation_file_path = "data/visualisation/"

keys = ['003', '004']

for key in keys:
    parse_proteomes(proteome_files_dir, data, key)
    data[key]['X'], data[key]['Y'] = shuffle(data[key]['X'], data[key]['Y'], random_state=1)

    write_to_file(data, key, 'X', 'Y', 1000, data[key]['FASTA'], False)

    filter_sequences(data, key, data[key]['embeddings'])

# Species were set 'empirically'
visualise_PCA_species(data, keys[0], visualisation_file_path+key+"_PCA.png", ['AQUAE', 'SACS2', 'THEMA'])
visualise_MDE_species(data, keys[0], visualisation_file_path+key+"_MDE.png")

visualise_PCA_species(data, keys[1], visualisation_file_path+key+"_PCA.png", ['9EURY', 'ECOLI', 'NITMS'])
visualise_MDE_species(data, keys[1], visualisation_file_path+key+"_MDE.png")