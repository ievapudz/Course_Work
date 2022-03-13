#!/usr/bin/env python3.7

# A script that draws PCA visualisation for aminoacid
# frequency dataset.

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pymde
import numpy
import torch
import pandas as pd
import matplotlib.pyplot as plt
from dataset_processing import create_data
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from Bio.SeqUtils.ProtParam import ProteinAnalysis

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

    for i in range(len(Ys)):
        if(int(Ys[i]) >= 65):
            Ys[i] = 1
        elif(int(Ys[i]) < 65):
            Ys[i] = 0

    analysed_seq = ProteinAnalysis(str(data[keys[0]]['X'][0].seq))
    aa_freq_columns = list(analysed_seq.count_amino_acids().keys())
    df = pd.DataFrame(Xs, columns=aa_freq_columns)
    df['temperature'] = Ys
   
    X=df.loc[:,aa_freq_columns].values
    Y=df.loc[:,'temperature'].values
    
    sc=StandardScaler()  
    X=sc.fit_transform(X) 

    pca = PCA(2)
    principalComponents=pca.fit_transform(X)
    principalDf=pd.DataFrame(data=principalComponents,columns=['principal component 1','principal component 2'])
    finalDf=pd.concat([principalDf,df[['temperature']]],axis=1)

    fig=plt.figure(figsize=(8,8))  
    ax=fig.add_subplot(1,1,1)  
    targets=[0, 1]
    colors=['b', 'r']
    for target, color in zip(targets,colors):    
        indicesToKeep = finalDf['temperature'] == target  
        ax.scatter(finalDf.loc[indicesToKeep,'principal component 1'],
              finalDf.loc[indicesToKeep,'principal component 2'],
             c=color,
             s=50)
    plt.savefig(plotpath, dpi=300)

def visualise_aminoacid_frequencies_MDE_PCA(data, keys, plotpath, colormap):
    [Xs, Ys] = get_aminoacid_frequencies_as_list(data, keys)

    for i in range(len(Ys)):
        if(int(Ys[i]) >= 65):
            Ys[i] = 1
        elif(int(Ys[i]) < 65):
           Ys[i] = 0

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = torch.from_numpy(Xs)
    pca_embedding = pymde.pca(Xs_torch, 20)
    pymde.plot(pca_embedding, color_by=Ys, savepath=plotpath, color_map=colormap, figsize_inches=(11, 10), marker_size=20.0)

print("Creating data object")
data = create_data('data/003/', dataset_names=['training_v2',
                                               'validation_v2',
                                               'testing_v2'])

visualise_aminoacid_frequencies_PCA(data, ['test'], 
                                    'data/003/visualisation_v2/003_testing_v2_aa_freq_PCA.png',
                                    two_color_cmap)

visualise_aminoacid_frequencies_MDE_PCA(data, ['test'],
                                    'data/003/visualisation_v2/003_testing_v2_aa_freq_MDE_PCA_3D.png',
                                    two_color_cmap)
