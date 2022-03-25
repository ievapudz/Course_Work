import numpy
import torch
import sys
import os

# A funtion that loads embeddings to dictionary of numpy arrays with according keywords
# Example keywords: ['x_train', 'y_train']
def load_numpy_from_NPZ(NPZ_file, keywords):
    dataset = {}
    with numpy.load(NPZ_file) as data_loaded:
        for i in range(len(keywords)):
            dataset[keywords[i]] = data_loaded[keywords[i]]
    return dataset

# A funtion that loads embeddings to dictionary with according keywords
# Example keywords: ['x_train', 'y_train']
def load_tensor_from_NPZ(NPZ_file, keywords):
    dataset = {}
    with numpy.load(NPZ_file, allow_pickle=True) as data_loaded:
        for i in range(len(keywords)):
            dataset[keywords[i]] = torch.from_numpy(data_loaded[keywords[i]])
    return dataset

# A function that trims the dataset so that its length would divide from the number of batches
def trim_dataset(dataset, keywords, batch_size):
    for i in range(len(keywords)):
        residual = len(dataset[keywords[i]]) % batch_size
        if(residual != 0):
            dataset[keywords[i]] = dataset[keywords[i]][0:len(dataset[keywords[i]])-residual]

# A function that converts non-binary labels to binary
def convert_labels_to_binary(dataset, keywords):
    for keyword in keywords:
        for i in range(len(dataset[keyword])):
            if(dataset[keyword][i].item() >= 65):
                dataset[keyword][i] = 1
            elif(dataset[keyword][i].item() < 65):
                dataset[keyword][i] = 0

# A function that normalises temperature labels
def normalise_labels(dataset, keywords, denominator):
    for keyword in keywords:
        normalised_labels = []
        for i in range(len(dataset[keyword])):
            float_tensor_normalised = torch.tensor(float(dataset[keyword][i].item() / denominator), dtype=torch.float32)
            normalised_labels.append(float_tensor_normalised)
        dataset[keyword] = torch.FloatTensor(normalised_labels)

# A function that normalises temperature labels to z-scores
def normalise_labels_as_z_scores(dataset, keywords, ref_point):
    # ref_point - by default, it is mean of sample to calculate z-score. 
    #             This function allows to calculate z-score from point other
    #             than the mean. 
    for keyword in keywords:
        normalised_labels = []
        std = standard_deviation(dataset[keyword], ref_point)
        for i in range(len(dataset[keyword])):
            float_tensor_normalised = torch.tensor(float((dataset[keyword][i].item() - ref_point) / std), dtype=torch.float32)
            normalised_labels.append(float_tensor_normalised)
        dataset[keyword] = torch.FloatTensor(normalised_labels)

# Conversion of z-score normalisation back to a temperature label
def convert_z_score_to_label(z_score_tensor, ref_point, std):
    # ref_point - by default, it is mean of sample to calculate z-score. 
    #             This function allows to calculate z-score from point other
    #             than the mean. 
    return torch.tensor(float(z_score_tensor.item() * std + ref_point), dtype=torch.float32)

# A function to calculate standard deviation
def standard_deviation(dataset, mean):
    N = len(dataset)
    var = 0
    for i in range(N):
        var += (float(dataset[i].item() - mean))**2
    var *= float(1/N)
    return var**(0.5)

