import os
import sys
import torch
import numpy
from Bio import SeqIO
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

"""
This module contains functions for dataset processing.

Requirements:
* biopython
* data.zip file that contains default proteomes
"""

def data_division():
    # Configuration
    temperature_labels_full = [37, 80]
    files = []

    if(sys.argv[1] == '-f'):
        # If the script is run in Colab environment
        files = ['data/proteomes/UP000000625_83333.fasta', 'data/proteomes/UP000001974_273057.fasta']
    elif(sys.argv == ''):
        # If the script is run as a part of UNIX pipeline, but no arguments were provided
        files = ['data/proteomes/UP000000625_83333.fasta', 'data/proteomes/UP000001974_273057.fasta']
    else:
        # If the script is run as a part of UNIX pipeline with arguments
        files = sys.argv[1:]

    # Initialisation of the dataset container
    data = {
        'train': {
            'X' : [],
            'Y' : [],
            'FASTA_prefix': 'data/FASTA/training_',
            'CSV_prefix': 'data/CSV/training_',
        },
        'validate': {
            'X' : [],
            'Y' : [],
            'FASTA_prefix': 'data/FASTA/validation_',
            'CSV_prefix': 'data/CSV/validation_'
        },
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA_prefix': 'data/FASTA/testing_',
            'CSV_prefix': 'data/CSV/testing_'
        }
    }

    # Removing duplicate sequences in the dataset
    seen = set()
    for i in range(len(temperature_labels_full)):
        records = [] 
        # Parsing sequences (X dataset) from one dataset 
        for record in SeqIO.parse(files[i], "fasta"):
            records.append(record)

        # Creating Y dataset from temperature labels 
        temperature_labels = [temperature_labels_full[i]] * len(records)

        # Spliting the dataset to 70% (training) and 30% (trying)
        X_train, X_try, Y_train, Y_try = train_test_split(records, temperature_labels, test_size=0.3, shuffle=True, random_state=1)

        # Splitting 30% from the initial set in half for calidation and testing
        X_validate, X_test, Y_validate, Y_test = train_test_split(X_try, Y_try, test_size=0.5, shuffle=True, random_state=1)

        data['train']['X'] = data['train']['X'] + X_train
        data['train']['Y'] = data['train']['Y'] + Y_train
        data['validate']['X'] = data['validate']['X'] + X_validate
        data['validate']['Y'] = data['validate']['Y'] + Y_validate
        data['test']['X'] = data['test']['X'] + X_test
        data['test']['Y'] = data['test']['Y'] + Y_test

    # Shuffling the datasets
    for element in data.keys():
        data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)

    return data

def create_data(dataset_dir_prefix):
    # dataset_dir_prefix - notes where the information about dataset is placed
    data = {
        'train': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/training/training.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/training/',
        },
        'validate': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/validation/validation.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/validation/',
        },
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/testing/testing.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/testing/',
        }
    }

    for key in data.keys():
        # Parsing sequences (X dataset) from one dataset 
        for record in SeqIO.parse(data[key]['FASTA'], "fasta"):
            data[key]['X'].append(record)
            data[key]['Y'].append(record.name.split('|')[2])

    # Shuffling the datasets
    for element in data.keys():
        data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)

    return data

def get_equal_proportions(data, key, overall_number, classes):
    expected_number = [int(overall_number/len(classes))] * len(classes)
    X_equal_proportions = []
    Y_equal_proportions = []
    for i in range(len(data[key]['X'])):
        for j in range(len(classes)):
            if(data[key]['Y'][i] == classes[j]):
                if(expected_number[j] > 0):
                    X_equal_proportions.append(data[key]['X'][i])
                    Y_equal_proportions.append(classes[j])
                    expected_number[j] -= 1
    
    data[key]['X_equally_proportioned'] = X_equal_proportions
    data[key]['Y_equally_proportioned'] = Y_equal_proportions

def filter_sequences(data, key, path_to_embeddings):
    embeddings_list = "embeddings_files.tmp"
    command = "ls -1 "+path_to_embeddings+" > "+embeddings_list
    os.system(command)

    emb_list_handle = open(embeddings_list, 'r')
    emb_list = emb_list_handle.readlines()
    emb_list_handle.close()
    emb_set = set()
    for j in range(len(emb_list)):
        emb_set.add(emb_list[j].split('.')[0])

    data[key]['X_filtered'] = []
    data[key]['Y_filtered'] = []    
    for i in range(len(data[key]['X'])):
        #if(data[key]['X'][i].id.split('|')[1] in emb_set):
        if(data[key]['X'][i].id in emb_set):
            data[key]['X_filtered'].append(data[key]['X'][i])
            data[key]['Y_filtered'].append(data[key]['Y'][i])

    command = "rm *.tmp"
    os.system(command)

def get_ESM_embeddings_as_list(data, keys):
    # This function gathers ESM embeddings to list representation

    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # output_file_path - path to the output file.
    EMB_LAYER = 33
    Ys = []
    Xs = []

    for key in keys:
        EMB_PATH = data[key]['embeddings']
        for i in range(len(data[key]['Y_filtered'])):
            Ys.append(data[key]['Y_filtered'][i])
            file_name = data[key]['X_filtered'][i].id.split('|')[1]
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])
    
    return [Xs, Ys]

def get_ESM_embeddings_as_list_with_ids(data, keys):
    # This function gathers ESM embeddings to list representation along with sequence ids

    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # output_file_path - path to the output file.
    EMB_LAYER = 33
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
    
    return [Xs, Ys, ids]

def get_tensor_from_list(Xs, Ys):
    Xs = torch.stack(Xs, dim=0).numpy()
    Xs_tensor = None
    Xs_tensor = torch.from_numpy(Xs)

    Ys_array = numpy.asarray(Ys)
    Ys_tensor = torch.from_numpy(Ys_array)

    return [Xs_tensor, Ys_tensor]

def get_ESM_embeddings_as_tensor(data, keys):
    [Xs, Ys] = get_ESM_embeddings_as_list(data, keys)
    [Xs_tensor, Ys_tensor] = get_tensor_from_list(Xs, Ys)
    return [Xs_tensor, Ys_tensor]
