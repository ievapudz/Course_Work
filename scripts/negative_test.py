#!/usr/bin/env python3.7

import os
from Bio import SeqIO
from sklearn.utils import shuffle
from file_actions import write_to_file
from dataset_processing import filter_sequences
from visualise_embeddings import visualise_multiple_MDE_species, visualise_multiple_PCA_species
from file_actions import parse_proteomes
from file_actions import generate_embeddings
from matplotlib.colors import ListedColormap

three_color_cmap = ListedColormap(["navy", "red", "green"])

data = {
    '003': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000798', 'UP000008183', 'UP000001974_273057'],
        'temperature_labels': [80, 80, 80],
        'FASTA': 'data/cluster_tests/003/FASTA/003.fasta',
        'embeddings': 'data/cluster_tests/003/EMB_ESM1b'
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

# Species were set 'empirically'
species = [['AQUAE', 'SACS2', 'THEMA'], ['9EURY', 'ECOLI', 'NITMS']]

for i in range(len(keys)):
    parse_proteomes(proteome_files_dir, data, keys[i])
    data[keys[i]]['X'], data[keys[i]]['Y'] = shuffle(data[keys[i]]['X'], data[keys[i]]['Y'], random_state=1)

    write_to_file(data, keys[i], 'X', 'Y', 1000, data[keys[i]]['FASTA'], False)

    filter_sequences(data, keys[i], data[keys[i]]['embeddings'])

    visualise_multiple_PCA_species(data, [keys[i]], visualisation_file_path+keys[i]+"_PCA.png", species[i], three_color_cmap)
    visualise_multiple_MDE_species(data, [keys[i]], visualisation_file_path+keys[i]+"_MDE.png", three_color_cmap)

