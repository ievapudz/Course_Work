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

def visualise_multiple_PCA(data, keys, plotpath, colormap, is_read_file_name_id=True):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        print('Visualising:', key)
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            Ys.append(data[key]['Y_filtered'][i])
            if is_read_file_name_id:
                file_name = data[key]['X_filtered'][i].id.split('|')[1]
            else:
                file_name = data[key]['X_filtered'][i].id
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    pca = PCA(60)
    Xs_train_pca = pca.fit_transform(Xs)

    fig_dims = (7, 6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sc = ax.scatter(Xs_train_pca[:,0], Xs_train_pca[:,1], c=Ys, marker='.', cmap=colormap)
    ax.set_xlabel('PCA first principal component')
    ax.set_ylabel('PCA second principal component')
    plt.colorbar(sc, label='Temperature labels', ticks=numpy.linspace(37, 80, 2))
    plt.savefig(plotpath, dpi=300)

def visualise_multiple_PCA_species(data, keys, plotpath, classes, colormap):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        print('Visualising:', key)
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            # For plot's Ys the organism species is taken
            for j in range(len(classes)):
                if(data[key]['X_filtered'][i].id.split('|')[2].split('_')[1]==classes[j]):
                    Ys.append(j)
            file_name = data[key]['X_filtered'][i].id.split('|')[1]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    pca = PCA(60)
    Xs_train_pca = pca.fit_transform(Xs)

    fig_dims = (7, 6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sc = ax.scatter(Xs_train_pca[:,0], Xs_train_pca[:,1], c=Ys, marker='.', cmap=colormap)
    ax.set_xlabel('PCA first principal component')
    ax.set_ylabel('PCA second principal component')
    
    cb = plt.colorbar(sc, label='Species', ticks=numpy.linspace(0, len(classes)-1, len(classes)))
    cb.ax.set_yticklabels(classes)
    plt.savefig(plotpath, dpi=300)

def visualise_multiple_MDE_PCA(data, keys, plotpath, colormap, is_read_file_name_id=True):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            Ys.append(data[key]['Y_filtered'][i])
            if is_read_file_name_id:
                file_name = data[key]['X_filtered'][i].id.split('|')[1]
            else:
                file_name = data[key]['X_filtered'][i].id
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])
    
    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = None
    Xs_torch = torch.from_numpy(Xs)
    pca_embedding = pymde.pca(Xs_torch, 1280)
    pymde.plot(pca_embedding, color_by=Ys, savepath=plotpath, color_map=colormap, figsize_inches=(11, 10), marker_size=20.0)

def visualise_multiple_MDE(data, keys, plotpath, colormap, is_read_file_name_id=True):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []

    for key in keys:
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            Ys.append(data[key]['Y_filtered'][i])
            if is_read_file_name_id:
                file_name = data[key]['X_filtered'][i].id.split('|')[1]
            else:
                file_name = data[key]['X_filtered'][i].id
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = None
    Xs_torch = torch.from_numpy(Xs)
    embedding = pymde.preserve_neighbors(Xs_torch, constraint=pymde.Standardized()).embed(verbose=True)
    pymde.rotate(embedding, 90)
    pymde.plot(embedding, color_by=Ys, savepath=plotpath, color_map=colormap, figsize_inches=(11, 10), marker_size=20.0)
    
def visualise_multiple_MDE_species(data, keys, plotpath, colormap):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # plotpath - path to the output plot.
    Ys = []
    Xs = []
    Xs_torch = None

    for key in keys:
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            # For plot's Ys the organism species is taken
            Ys.append(data[key]['X_filtered'][i].id.split('|')[2].split('_')[1])
            file_name = data[key]['X_filtered'][i].id.split('|')[1]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])

    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_torch = torch.from_numpy(Xs)
    embedding = pymde.preserve_neighbors(Xs_torch, init='quadratic', constraint=pymde.Standardized()).embed(verbose=True)
    pymde.plot(embedding, color_by=Ys, savepath=plotpath, color_map=colormap, figsize_inches=(11, 10), marker_size=20.0)

