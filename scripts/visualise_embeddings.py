import esm
import torch
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import pymde
from sklearn.decomposition import PCA
from matplotlib import colors
from matplotlib.colors import ListedColormap

EMB_LAYER = 33
custom_cmap = ListedColormap(["navy", "pink"])

def visualise_PCA(data, keys, plotpath):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        FASTA_PATH = data[key]['FASTA_prefix']+'sequences.fasta'
        EMB_PATH = data[key]['embeddings']
        for header, _seq in esm.data.read_fasta(FASTA_PATH):
            temperature_label = header.split('|')[-1]
            Ys.append(int(temperature_label))
            file_name = header.split('|')[0][1:]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    pca = PCA(60)
    Xs_train_pca = pca.fit_transform(Xs)

    fig_dims = (7, 6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sc = ax.scatter(Xs_train_pca[:,0], Xs_train_pca[:,1], c=Ys, marker='.', cmap=custom_cmap)
    ax.set_xlabel('PCA first principal component')
    ax.set_ylabel('PCA second principal component')
    plt.colorbar(sc, label='Variant Effect', ticks=numpy.linspace(37, 80, 2))
    plt.savefig(plotpath)

def visualise_MDE(data, keys, plotpath):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        FASTA_PATH = data[key]['FASTA_prefix']+'sequences.fasta'
        EMB_PATH = data[key]['embeddings']
        for header, _seq in esm.data.read_fasta(FASTA_PATH):
            temperature_label = header.split('|')[-1]
            Ys.append(int(temperature_label))
            file_name = header.split('|')[0][1:]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = None
    Xs_torch = torch.from_numpy(Xs)
    embedding = pymde.preserve_neighbors(Xs_torch).embed(verbose=True)
    pymde.plot(embedding, color_by=Ys, savepath=plotpath, color_map=custom_cmap)