import os
from os.path import exists
import sys
import torch
import numpy
import random
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

def create_data(dataset_dir_prefix, dataset_names=['training', 'validation', 'testing']):
    # dataset_dir_prefix - notes where the information about dataset is placed
    # dataset_names - names of the dataset partitions
    data = {
        'train': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/'+dataset_names[0]+'/'+dataset_names[0]+'.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/'+dataset_names[0]+'/',
        },
        'validate': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/'+dataset_names[1]+'/'+dataset_names[1]+'.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/'+dataset_names[1]+'/',
        },
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/'+dataset_names[2]+'/'+dataset_names[2]+'.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/'+dataset_names[2]+'/',
        }
    }

    for key in data.keys():
        if(exists(data[key]['FASTA'])):
            # Parsing sequences (X dataset) from one dataset 
            for record in SeqIO.parse(data[key]['FASTA'], "fasta"):
                data[key]['X'].append(record)
                data[key]['Y'].append(record.name.split('|')[2])

    # Shuffling the datasets
    for element in data.keys():
        temp = list(zip(data[element]['X'], data[element]['Y']))
        random.shuffle(temp)
        data[element]['X'], data[element]['Y'] = zip(*temp)

    return data

def create_testing_data(dataset_dir_prefix, dataset_parent_dir=['testing'], 
                        dataset_names=['testing'], labelled=True):
    # dataset_dir_prefix - notes where the information about dataset is placed
    # dataset_names - names of the dataset partitions
    
    data = {
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_dir_prefix+'FASTA/'+dataset_parent_dir[0]+'/'+dataset_names[0]+'.fasta',
            'embeddings': dataset_dir_prefix+'EMB_ESM1b/'+dataset_names[0]+'/',
        }
    }

    for key in data.keys():
        if(exists(data[key]['FASTA'])):
            # Parsing sequences (X dataset) from one dataset 
            for record in SeqIO.parse(data[key]['FASTA'], "fasta"):
                data[key]['X'].append(record)
                if(labelled):
                    data[key]['Y'].append(record.name.split('|')[2])
                else:
                    data[key]['Y'].append(0)

    # Shuffling the datasets
    for element in data.keys():
        if(labelled):
            data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)
        else:
            data[element]['X'] = shuffle(data[element]['X'], random_state=1)

    return data

# Rewritten create_testing_data function more suitable for automatic flow
def create_testing_data_2(dataset_FASTA, dataset_embeddings_dir, labelled=True):
    # dataset_FASTA - FASTA file with sequences for testing dataset
    # dataset_embeddings_dir - directory with all generated testing embeddings
    # labelled - flag to determine whether the data is labelled or not

    data = {
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA': dataset_FASTA,
            'embeddings': dataset_embeddings_dir+'/',
        }
    }

    for key in data.keys():
        if(exists(data[key]['FASTA'])):
            # Parsing sequences (X dataset) from one dataset 
            for record in SeqIO.parse(data[key]['FASTA'], "fasta"):
                data[key]['X'].append(record)
                if(labelled):
                    data[key]['Y'].append(record.name.split('|')[2])
                else:
                    data[key]['Y'].append(0)

    # Shuffling the datasets
    for element in data.keys():
        if(labelled):
            data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)
        else:
            data[element]['X'] = shuffle(data[element]['X'], random_state=1)

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

def filter_sequences(data, key, path_to_embeddings, labelled=True):
    embeddings_list = "embeddings_files.tmp"
    command = "ls -1 "+path_to_embeddings+" | sort > "+embeddings_list
    os.system(command)

    emb_list_handle = open(embeddings_list, 'r')
    emb_list = emb_list_handle.readlines()
    emb_list_handle.close()
    emb_set = set()   
 
    for j in range(len(emb_list)):
        emb_set.add(emb_list[j].split('.pt')[0])

    data[key]['X_filtered'] = []
    data[key]['Y_filtered'] = []
    
    for i in range(len(data[key]['X'])):
        if(data[key]['X'][i].id in emb_set):
            data[key]['X_filtered'].append(data[key]['X'][i])
            if(labelled):
                data[key]['Y_filtered'].append(data[key]['Y'][i])
            else:
                data[key]['Y_filtered'].append(0)

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
        for i in range(len(data[key]['X_filtered'])):
            Ys.append(data[key]['Y_filtered'][i])

            file_name = data[key]['X_filtered'][i].id
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)
            Xs.append(embs['mean_representations'][EMB_LAYER])
    
    return [Xs, Ys]

def get_ESM_embeddings_as_list_with_ids(data, keys):
    # This function gathers ESM embeddings to list representation along with sequence ids

    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    
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

    if(len(Ys)):
        Ys_array = numpy.asarray(Ys)
        Ys_array = Ys_array.astype('int32')
        Ys_tensor = torch.from_numpy(Ys_array)
        return [Xs_tensor, Ys_tensor]
    else:
        return [Xs_tensor, None]

def get_ESM_embeddings_as_tensor(data, keys):
    [Xs, Ys] = get_ESM_embeddings_as_list(data, keys)
    [Xs_tensor, Ys_tensor] = get_tensor_from_list(Xs, Ys)

    return [Xs_tensor, Ys_tensor]

# Embedding joining
def join_embeddings(data, keys, dims=1280):
    # data - is an array of data objects that keep information about
    #        divided protein sequences.
    EMB_LAYER = 33

    number_of_sequences = len(data[0][keys[0]]['Y_filtered'])
    joined_Xs = torch.zeros([number_of_sequences, dims])
    joined_Ys = []
    
    for i in range(number_of_sequences):
        joined_Ys.append(data[0][keys[0]]['Y_filtered'][i])

        Xs_accum = torch.zeros([dims])
        overall_seq_length = 0

        for data_object in data:
            EMB_PATH = data_object[keys[0]]['embeddings']
            file_name = data_object[keys[0]]['X_filtered'][i].id
            fn = f'{EMB_PATH}/{file_name}.pt'
            embs = torch.load(fn)

            Xs = torch.mul(embs['mean_representations'][EMB_LAYER], 
                           len(data_object[keys[0]]['X_filtered'][i].seq))
            Xs_accum = torch.add(Xs_accum, Xs)
            overall_seq_length += len(data_object[keys[0]]['X_filtered'][i].seq)

        Xs_accum = torch.div(Xs_accum, overall_seq_length)
        joined_Xs[i] = Xs_accum

    return [joined_Xs, joined_Ys]

def get_list_of_proteomes(directory, range_regex):
    random.seed(27)

    tmp_file = 'out.tmp'
    command_code = os.system('ls '+directory+' | egrep "'+range_regex+'" > '+tmp_file)

    proteomes_str = ''
    if(command_code == 0):
        file_handle = open(tmp_file, 'r')
        proteomes_str = file_handle.read()
        file_handle.close()
        os.remove(tmp_file)

    proteomes = proteomes_str.split('\n')
    proteomes.remove('')
    random.shuffle(proteomes)

    return proteomes

# Filtering sequences in the proteomes by length threshold
def filter_sequences_by_length_before_embeddings(proteomes, directory, threshold=1022):
    filtered_sequences = {}

    for proteome in proteomes:
        filtered_sequences[proteome] = []
        for index, record in enumerate(SeqIO.parse(directory+'/'+proteome, "fasta")):
            if(len(record.seq) <= threshold):
                record.name = proteome.split('.')[0]
                filtered_sequences[proteome].append(record)

    return filtered_sequences

# Checking, whether the dataset successfully fills up with proteomes
def fill_model_sets(proteomes, filtered_sequences, range_regex, max_seq_in_prot, capacity,
                    proportions, threshold):

    set_names = ['train', 'validate', 'test']
    sets = { 
        set_names[0]: [],
        set_names[1]: [],
        set_names[2]: []
    }

    capacities = [proportion*capacity for proportion in proportions]
    proteomes_track = list(proteomes)

    for i_cap, cap in enumerate(capacities):
        for proteome in proteomes:    
            if(proteome in proteomes_track and len(sets[set_names[i_cap]]) < cap):
                for index, record in enumerate(filtered_sequences[proteome]):
                    if(index < len(filtered_sequences[proteome]) and index < max_seq_in_prot and len(sets[set_names[i_cap]]) < cap):
                        record.name = proteome.split('.')[0]
                        sets[set_names[i_cap]].append(record)
                    elif(len(sets[set_names[i_cap]]) >= cap):
                        if(proteome in proteomes_track):
                            proteomes_track.remove(proteome)
                        break                  
                    elif(index >= max_seq_in_prot):
                        if(proteome in proteomes_track):
                            proteomes_track.remove(proteome)
                        break
                if(len(filtered_sequences[proteome]) < max_seq_in_prot):
                    if(proteome in proteomes_track):
                        proteomes_track.remove(proteome)
                    continue
            elif(len(sets[set_names[i_cap]]) == cap):
                break
  
    prots_in_sets = [ set(), set(), set() ]

    for i, name in enumerate(set_names):
        for record in sets[name]:
            prots_in_sets[i].add(record.name)
 
    fill_success = 'success'
    for i, name in enumerate(set_names):
        if(len(sets[name]) < capacities[i]):
            fill_success = 'failure'
            break
    """
    print('training') 
    for record in sets['train']:
        print(record.name)

    print('validation')
    for record in sets['validate']:
        print(record.name)

    print('testing')
    for record in sets['test']:
        print(record.name)
    """

    print(str(max_seq_in_prot)+'\t'+range_regex+'\t'+str(len(sets['train']))+'\t'+\
          str(len(sets['validate']))+'\t'+str(len(sets['test']))+'\t'+fill_success+'\t'+\
          str(len(prots_in_sets[0]))+'\t'+str(len(prots_in_sets[1]))+'\t'+\
          str(len(prots_in_sets[2])))
	
