#!/usr/bin/env python3.7

# This is a script that generates vectors composed of 20 numbers that
# note the relative frequency of each type aminoacid in the sequence.

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import torch
import numpy
import matplotlib.pyplot as plt
from Bio import SeqIO
from sklearn.decomposition import PCA
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from dataset_processing import create_data
from dataset_processing import get_tensor_from_list
from file_actions import save_tensors_as_NPZ
from file_actions import print_tensors_as_SV_to_file
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler

two_color_cmap = ListedColormap(["navy", "red"])

def get_aminoacid_frequencies_as_list(data, keys):
    Ys = []
    Xs = []
    for key in keys:
        for i in range(len(data[key]['X'])):
            Ys.append(data[key]['Y'][i])
            analysed_seq = ProteinAnalysis(str(data[key]['X'][i].seq))
            aa_freqs = analysed_seq.get_amino_acids_percent()
            aa_freq_tensor = torch.tensor(list(aa_freqs.values()))
            Xs.append(aa_freq_tensor)

    return [Xs, Ys]

def get_aminoacid_frequencies_as_tensor(data, keys):
    [Xs, Ys] = get_aminoacid_frequencies_as_list(data, keys)
    [Xs_tensor, Ys_tensor] = get_tensor_from_list(Xs, Ys)
    return [Xs_tensor, Ys_tensor]

def visualise_aminoacid_frequencies_PCA(data, keys, plotpath, colormap):
    [Xs, Ys] = get_aminoacid_frequencies_as_list(data, keys)

    pca = PCA(2)
    Xs_scale = scaler.transform(Xs)
    Xs_pca = pca.fit_transform(Xs_scale)
    #Xs_pca_c = numpy.ascontiguousarray(Xs_pca, dtype=numpy.float32)    
    finalDf = pand.concat([principalDf, Ys, axis = 1)    


    print("Visualisation") 
    fig_dims = (7, 6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sc = ax.scatter(Xs_pca_c[:,0], Xs_pca_c[:,1], c=Ys, marker='.', cmap=colormap)
    ax.set_xlabel('PCA first principal component')
    ax.set_ylabel('PCA second principal component')
    plt.colorbar(sc, label='Temperature labels', ticks=numpy.linspace(37, 80, 2))
    plt.savefig(plotpath, dpi=300)

print("Creating data object")
data = create_data('data/003/', dataset_names=['training_v2',
                                               'validation_v2',
                                               'testing_v2'])

#print("Converting aminoacid frequencies (training) to tensor")
#[Xs_train_tensor, Ys_train_tensor] = get_aminoacid_frequencies_as_tensor(data,
#                                     ['train'])

print("Converting aminoacid frequencies (validation) to tensor")
[Xs_validate_tensor, Ys_validate_tensor] = get_aminoacid_frequencies_as_tensor(data,
                                                                  ['validate'])
print("Visualising aminoacid frequencies vectors")
visualise_aminoacid_frequencies_PCA(data, ['validate'], 
                                    'data/003/visualisation_v2/validation_v2_aa_freqs_PCA.png', 
                                    two_color_cmap) 
"""
print("Saving tensors to NPZ file")
save_tensors_as_NPZ([Xs_train_tensor, Ys_train_tensor,
                     Xs_validate_tensor, Ys_validate_tensor],
                    ['x_train', 'y_train', 'x_validate', 'y_validate'],
                    'data/003/NPZ/training_and_validation_aa_freq_v2.npz')

data_train_tensor = { 'x_train': Xs_train_tensor, 'y_train': Ys_train_tensor }

print("Saving training tensors to a TSV file")
print_tensors_as_SV_to_file(data, data_train_tensor, 'train', ['x_train', 'y_train'],
                            dim=20, subkey='X',
                            out_file_name='data/003/TSV/training_v2_aa_freq_tensors.tsv',
                            sep="\t", labelled=True)

data_validate_tensor = { 'x_validate': Xs_validate_tensor, 'y_validate': Ys_validate_tensor }

print("Saving validation tensors to a TSV file")
print_tensors_as_SV_to_file(data, data_validate_tensor, 'validate', ['x_validate', 'y_validate'],
                            dim=20, subkey='X',
                            out_file_name='data/003/TSV/validation_v2_aa_freq_tensors.tsv',
                            sep="\t", labelled=True)
"""
