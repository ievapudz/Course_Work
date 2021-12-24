#!/usr/bin/env python3.7

import os
from Bio import SeqIO
from sklearn.utils import shuffle
from dataset_processing import filter_sequences
from dataset_processing import get_equal_proportions
from visualise_embeddings import visualise_multiple_PCA
from visualise_embeddings import visualise_multiple_MDE
from file_actions import write_to_file
from file_actions import parse_proteomes
from file_actions import generate_embeddings
from matplotlib.colors import ListedColormap

two_color_cmap = ListedColormap(["navy", "red"])

data = {
    '001': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000625_83333', 'UP000000798', 'UP000008183'],
        'temperature_labels': [37, 80, 80],
        'FASTA': 'data/cluster_tests/001/FASTA/001_',
        'embeddings': 'data/cluster_tests/001/EMB_ESM1b'
    },
    '002': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000077428', 'UP000000792', 'UP000001974_273057'],
        'temperature_labels': [37, 37, 80],
        'FASTA': 'data/cluster_tests/002/FASTA/002.fasta',
        'embeddings': 'data/cluster_tests/002/EMB_ESM1b/'
    }
}

proteome_files_dir = 'data/001/proteomes/'
visualisation_file_path = 'data/cluster_tests/visualisation/'

keys = ['001', '002']
for key in keys:
    parse_proteomes(proteome_files_dir, data, key)
    data[key]['X'], data[key]['Y'] = shuffle(data[key]['X'], data[key]['Y'], random_state=1)

    # Checking how many sequences of each class there is in a sample
    print('Number of each class:', data[key]['Y'][0:1000].count(37), data[key]['Y'][0:1000].count(80))

    get_equal_proportions(data, key, 1000, [37, 80])

    # Checking how many sequences of each class there is in a sample
    print('Number of each class (eq):', data[key]['Y_equally_proportioned'][0:1000].count(37), data[key]['Y_equally_proportioned'][0:1000].count(80))

    write_to_file(data, key, 'X_equally_proportioned', 'Y_equally_proportioned', 1000, data[key]['FASTA'], False)

    filter_sequences(data, key, data[key]['embeddings'])
    
    visualise_multiple_PCA(data, [key], visualisation_file_path+key+"_PCA.png", two_color_cmap)
    visualise_multiple_MDE(data, [key], visualisation_file_path+key+"_MDE.png", two_color_cmap)