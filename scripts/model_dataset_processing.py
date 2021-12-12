import numpy
import torch

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
    with numpy.load(NPZ_file) as data_loaded:
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
def convert_labels_to_binary(dataset, keywords, original_labels):
    for keyword in keywords:
        for i in range(len(dataset[keyword])):
            if(dataset[keyword][i] == original_labels[1]):
                dataset[keyword][i] = 1
            elif(dataset[keyword][i] == original_labels[0]):
                dataset[keyword][i] = 0


