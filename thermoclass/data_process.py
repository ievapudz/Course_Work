import os
import torch
import numpy
from os.path import exists
from Bio import SeqIO
from sklearn.utils import shuffle

# Function that returns data object for inference flow
def create_testing_data(dataset_FASTA, dataset_embeddings_dir, labelled=True):
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
                    data[key]['Y'].append(None)

    # Shuffling the datasets
    for element in data.keys():
        if(labelled):
            data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)
        else:
            data[element]['X'] = shuffle(data[element]['X'], random_state=1)

    return data

# Filtering sequences that do not have their embeddings generated
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

# Gathering ESM embeddings to a list representation
def get_ESM_embeddings_as_list(data, keys):
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

# Converting the input list to a tensor
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

# Converting ESM embeddings to a tensor
def get_ESM_embeddings_as_tensor(data, keys):
    [Xs, Ys] = get_ESM_embeddings_as_list(data, keys)
    [Xs_tensor, Ys_tensor] = get_tensor_from_list(Xs, Ys)

    return [Xs_tensor, Ys_tensor]

# Saving tensors to an NPZ file
def save_tensors_as_NPZ(data_tensors, names_array, output_file_path):
    # data_tensors - an array that contains tensor arrays to save to `output_file_path`
    # names_array - an array that contains keywords for corresponding tensors
    numpy.savez(output_file_path, **{name:value for name,value in zip(names_array,data_tensors)})

# Printing tensors to a *SV file
def print_tensors_as_SV_to_file(data, data_tensor, key_data, keys_tensor,
                                dim=1280, subkey='X_filtered', out_file_name='',
                                sep=',', labelled=True):
    file_handle = open(out_file_name, "w")
    for i in range(len(data_tensor[keys_tensor[0]])):
        if(labelled):
            record = get_id_as_SV(data, i, key_data, 0, subkey=subkey, sep=sep) + \
                     get_id_as_SV(data, i, key_data, 1, subkey=subkey, sep=sep) + \
                     get_sequence_length_as_SV(data, i, key_data, subkey=subkey,
                                                sep=sep) + \
                     get_temperature_label_as_SV(data_tensor, i,
                                                  keys_tensor[1],
                                                  sep=sep, last_value=False) + \
                     get_embeddings_tensor_as_SV(data_tensor, i,
                                                  keys_tensor[0], dim=dim,
                                                  sep=sep, last_value=True)
        else:
            record = data[key_data][subkey][i].name + sep + \
                     data[key_data][subkey][i].seq + sep + \
                     get_sequence_length_as_SV(data, i, key_data, subkey=subkey, sep=sep) + \
                     get_embeddings_tensor_as_SV(data_tensor, i, keys_tensor[0],
                                                  dim=dim, sep=sep, last_value=True)
        file_handle.write(str(record)+"\n")

    file_handle.close()

# Returning the required identificator (property) from the sequence's header
def get_id_as_SV(data, index, key, id_index, subkey='X_filtered', sep=',', last_value=False):
    # data - an object with sequences in FASTA format
    # index - the index of record in data object
    # key - the chosen key of an inside of data object
    # id_index - index that determines which part of FASTA header is taken 
    #        0 - taxonomy ID
    #        1 - protein ID
    #        2 - temperature label
    identificator = data[key][subkey][index].name.split('|')[id_index]

    if last_value:
        return identificator
    else:
        return identificator + sep

# A Processing embeddings to be represented in SV format
def get_embeddings_tensor_as_SV(data, embedding_tensor_index, key, dim=1280, sep=',',
                                 last_value=False):
    record = ''
    for j in range(dim):
        embeddings_element = f"{data[key][embedding_tensor_index][j].item():{6}.{3}}"
        record = record + embeddings_element

        if j == dim-1 and not last_value:
            record = record + sep
        elif j == dim-1 and last_value:
            record = record
        else:
            record = record + sep

    return record

# Processing temperature labels to be represented in SV format
def get_temperature_label_as_SV(data, embedding_tensor_index, key,
                             sep, last_value=True):
    temperature_label = str(data[key][embedding_tensor_index].item())

    if last_value:
        return temperature_label
    else:
        return temperature_label + sep

# Returning the sequence length for SV
def get_sequence_length_as_SV(data, index, key, subkey='X_filtered',
                               sep=',', last_value=False):
    # data - an object with sequences in FASTA format
    # index - the index of record in data object
    # key - the chosen key of an inside of data object
    sequence_length = str(len(data[key][subkey][index].seq))
    if last_value:
        return sequence_length
    else:
        return sequence_length + sep

