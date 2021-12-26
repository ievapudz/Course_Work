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
from file_actions import parse_dataset
from file_actions import generate_embeddings
from matplotlib.colors import ListedColormap

two_color_cmap = ListedColormap(["navy", "red"])

data = {
    '002_train': {
        'X': [],
        'Y': [],
        'FASTA': 'data/002/FASTA/training/training.fasta',
        'embeddings': 'data/002/EMB_ESM1b/training'
    }
}

visualisation_file_path = 'data/002/visualisation/'

keys = ['002_train']
for key in keys:
    parse_dataset(data, key, 2)
    filter_sequences(data, key, data[key]['embeddings'])
    visualise_multiple_PCA(data, [key], visualisation_file_path+key+"_PCA.png", two_color_cmap, False)
    visualise_multiple_MDE(data, [key], visualisation_file_path+key+"_MDE.png", two_color_cmap, False)