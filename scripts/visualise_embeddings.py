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
custom_cmap = ListedColormap(["navy", "red"])

def visualise_PCA(data, key, plotpath):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    #for key in keys:
    print('Visualising:', key)
    EMB_PATH = data[key]['embeddings']
    for i in range(len(data[key]['Y_filtered'])):
        Ys.append(data[key]['Y_filtered'][i])
        file_name = data[key]['X_filtered'][i].id.split('|')[1]
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
    

def visualise_MDE(data, key, plotpath):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    EMB_PATH = data[key]['embeddings']
    for i in range(len(data[key]['Y_filtered'])):
        Ys.append(data[key]['Y_filtered'][i])
        file_name = data[key]['X_filtered'][i].id.split('|')[1]
        fn = f'{EMB_PATH}/{file_name}.pt'
        embs = torch.load(fn)
        Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = None
    Xs_torch = torch.from_numpy(Xs)
    embedding = pymde.preserve_neighbors(Xs_torch).embed(verbose=True)
    pymde.plot(embedding, color_by=Ys, savepath=plotpath, color_map=custom_cmap, figsize_inches=(8.8, 8.0))