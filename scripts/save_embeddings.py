import esm
import torch
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import pymde
from matplotlib import colors
from matplotlib.colors import ListedColormap

from file_actions import parse_proteomes
from file_actions import write_to_file
from dataset_processing import get_equal_proportions
from dataset_processing import filter_sequences

from sklearn.utils import shuffle

EMB_LAYER = 33

def save_MDE_embedding(data, keys, output_file_path):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # output_file_path - path to the output file.
    Ys = []
    Xs = []

    ids = []

    for key in keys:
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            ids.append(data[key]['X_filtered'][i].id)
            Ys.append(data[key]['Y_filtered'][i])
            file_name = data[key]['X_filtered'][i].id.split('|')[1]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = None
    Xs_torch = torch.from_numpy(Xs)
    embedding = pymde.preserve_neighbors(Xs_torch, constraint=pymde.Standardized()).embed(verbose=True)
    
    f = open(output_file_path, "w")
    for i in range(len(embedding)):
        out_line = ids[i]+"\t"+str(Ys[i])+"\t"+str(embedding[i][0].item())+"\t"+str(embedding[i][1].item())+"\t"+"\n"
        f.write(out_line)
    f.close()

############################################################################################################

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
    },
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

keys = ['001', '002']
for key in keys:
    parse_proteomes(proteome_files_dir, data, key)
    data[key]['X'], data[key]['Y'] = shuffle(data[key]['X'], data[key]['Y'], random_state=1)
    get_equal_proportions(data, key, 1000, [37, 80])
    write_to_file(data, key, 'X_equally_proportioned', 'Y_equally_proportioned', 1000, data[key]['FASTA'], False)
    filter_sequences(data, key, data[key]['embeddings'])
    save_MDE_embedding(data, [key], "data/cluster_tests/"+key+"/"+key+"_coordinates.tsv")

keys = ['003', '004']
for i in range(len(keys)):
    parse_proteomes(proteome_files_dir, data, keys[i])
    data[keys[i]]['X'], data[keys[i]]['Y'] = shuffle(data[keys[i]]['X'], data[keys[i]]['Y'], random_state=1)
    write_to_file(data, keys[i], 'X', 'Y', 1000, data[keys[i]]['FASTA'], False)
    filter_sequences(data, keys[i], data[keys[i]]['embeddings'])

save_MDE_embedding(data, ['003', '004'], "data/cluster_tests/005/005_coordinates.tsv")