#!/usr/bin/env python3.7

# A script that visualises the 003 datasets (separately)

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from Bio import SeqIO
from dataset_processing import filter_sequences
from visualise_embeddings import visualise_multiple_MDE_PCA
from visualise_embeddings import visualise_multiple_MDE
from visualise_embeddings import visualise_multiple_PCA
from file_actions import parse_dataset
from file_actions import generate_embeddings
from matplotlib.colors import ListedColormap

two_color_cmap = ListedColormap(["navy", "red"])

print("Creating data object")
data = {
    '003_train_v2': {
        'X': [],
        'Y': [],
        'FASTA': 'data/003/FASTA/training_v2/training_v2.fasta',
        'embeddings': 'data/003/EMB_ESM1b/training_v2'
    },
    '003_validate_v2': {
        'X': [],
        'Y': [],
        'FASTA': 'data/003/FASTA/validation_v2/validation_v2.fasta',
        'embeddings': 'data/003/EMB_ESM1b/validation_v2'
    },
    '003_test_v2': {
        'X': [],
        'Y': [],
        'FASTA': 'data/003/FASTA/testing_v2/testing_v2.fasta',
        'embeddings': 'data/003/EMB_ESM1b/testing_v2'
    }
}

visualisation_file_path = 'data/003/visualisation_v2/'

keys = ['003_test_v2']
for key in keys:
    print("Parsing dataset: "+key)
    parse_dataset(data, key, 2)
    print("Filtering sequences: "+key)
    filter_sequences(data, key, data[key]['embeddings'])
    print("Visualising PCA: "+key)
    visualise_multiple_PCA(data, [key], visualisation_file_path+key+"_PCA_Fortran.png", two_color_cmap, False)
    visualise_multiple_PCA(data, [key], visualisation_file_path+key+"_PCA_C.png", two_color_cmap, False)
    #print("Visualising MDE PCA: "+key)
    #visualise_multiple_MDE_PCA(data, [key], visualisation_file_path+key+"_MDE_PCA.png", two_color_cmap, False)
    #print("Visualising MDE: "+key)
    #visualise_multiple_MDE(data, [key], visualisation_file_path+key+"_MDE.png", two_color_cmap, False)
