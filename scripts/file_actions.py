import os
import numpy
import pymde
import torch
import csv
import math
from Bio import SeqIO
from dataset_processing import get_ESM_embeddings_as_list_with_ids
from dataset_processing import get_tensor_from_list

"The module that contains elements of workflow with files."

def create_division_FASTA(data):
    for element in data.keys():
        file_name = data[element]['FASTA_prefix']+'sequences.fasta'
        file_handle = open(file_name, 'w')
        for i in range(len(data[element]['X'])):
            file_handle.write('>'+data[element]['X'][i].name.split('|')[1]+'|'+str(data[element]['Y'][i]))
            file_handle.write("\n")
            file_handle.write(str(data[element]['X'][i].seq))
            file_handle.write("\n")
        file_handle.close()

def write_to_file(data, key, X_key, Y_key, headn, file_name, modify_name):
    # modify_name - boolean that determines wehther to add label to the header or not
    file_handle = open(file_name, 'w')
    for i in range(headn):
        if(modify_name):
            file_handle.write(data[key][X_key][i].name+'|'+str(data[key][Y_key][i])+"\n"+str(data[key][X_key][i].seq)+"\n")
        else:
            file_handle.write(data[key][X_key][i].name+"\n"+str(data[key][X_key][i].seq)+"\n")
    file_handle.close()

def parse_proteomes(proteome_files_dir, data, key):
    for i in range(len(data[key]['proteomes'])):
        for record in SeqIO.parse(proteome_files_dir+data[key]['proteomes'][i]+'.fasta', "fasta"):
            processed_record_name = '>'+record.name.split('|')[1]
            record.name = processed_record_name
            data[key]['X'].append(record)
            data[key]['Y'].append(data[key]['temperature_labels'][i])

# A function that parses FASTA records from dataset
def parse_dataset(data, key, temp_label_index):
    # data - dictionary with 'FASTA' key with file, where FASTA records are placed
    #        those FASTA records should have the temperature label in their headers.
    for record in SeqIO.parse(data[key]['FASTA'], 'fasta'):
        temp_label = record.name.split('|')[temp_label_index]
        if int(temp_label) >= 65:
            data[key]['Y'].append(1)
        else:
            data[key]['Y'].append(0)
        data[key]['X'].append(record)
        
def generate_embeddings(path_to_esm_extract, path_to_FASTA, path_to_embeddings):
    # Required PyTorch
    command = "python3.7 "+path_to_esm_extract+" esm1b_t33_650M_UR50S "+path_to_FASTA+" "+path_to_embeddings+" --repr_layers 0 32 33 --include mean per_tok"
    os.system(command)

def save_tensors_as_NPZ(data_tensors, names_array, output_file_path):
    # data_tensors - an array that contains tensor arrays to save to `output_file_path`
    # names_array - an array that contains keywords for corresponding tensors
    numpy.savez(output_file_path, **{name:value for name,value in zip(names_array,data_tensors)})

def save_MDE_as_TSV(data, keys, output_file_path):
    # data - dictionary that was created by filter_sequences function.
    # keys - array of the sets that need to be visualised in one plot.
    # output_file_path - path to the output file.
    [Xs, Ys, ids] = get_ESM_embeddings_as_list_with_ids(data, keys)
    [Xs_torch, Ys_torch] = get_tensor_from_list(Xs, Ys)

    embedding = pymde.preserve_neighbors(Xs_torch, constraint=pymde.Standardized()).embed(verbose=True)
    
    f = open(output_file_path, "w")
    for i in range(len(embedding)):
        out_line = ids[i]+"\t"+str(Ys[i])+"\t"+str(embedding[i][0].item())+"\t"+str(embedding[i][1].item())+"\t"+"\n"
        f.write(out_line)
    f.close()

# This function loads Tensor data from the specified NPZ file
def load_tensor_data_from_NPZ(NPZ_file_name, data_subset_keyword):
    dataset = {}
    with numpy.load(NPZ_file_name) as data_loaded:
        dataset[data_subset_keyword] = torch.from_numpy(data_loaded[data_subset_keyword])
    return dataset

# A function that prints a list of tensors to file
def print_tensor_elements(dataset, keys, out_file):
    # dataset - a list of lists with tensors
    # key - a list identifier
    # out_file - the name of output list file
    file_handle = open(out_file, 'w')
    for key in keys:
        for el in dataset[key]:
            file_handle.write(str(el.item())+"\n")
    file_handle.close()

# A function that prints embedding with its temperature label as CSV
def print_tensor_as_CSV(data, data_tensor, key_data, keys_tensor):
    # data - a dictionary that contains keys for which values are embeddings and temperature label
    # keys - an array with a key pair: ['x_set', 'y_set']
    for i in range(len(data_tensor[keys_tensor[0]])):
        record = get_id_as_CSV(data, i, key_data, 0) + get_id_as_CSV(data, i, key_data, 1) + get_sequence_length_as_CSV(data, i, key_data) + get_temperature_label_as_CSV(data_tensor, i, keys_tensor[1], False) + get_embeddings_tensor_as_CSV(data_tensor, i, keys_tensor[0], True)
        print(record)

# A function that returns the sequence length for CSV
def get_sequence_length_as_CSV(data, index, key, last_value=False):
    # data - an object with sequences in FASTA format
    # index - the index of record in data object
    # key - the chosen key of an inside of data object
    sequence_length = str(len(data[key]['X'][index].seq))
    if last_value:
        return sequence_length
    else:
        return sequence_length + ', '

# A function that returns the needed identificator (property) of the sequence from the header
def get_id_as_CSV(data, index, key, id_index, last_value=False):
    # data - an object with sequences in FASTA format
    # index - the index of record in data object
    # key - the chosen key of an inside of data object
    # id_index - index that determines which part of FASTA header is taken 
    #        0 - taxonomy ID
    #        1 - protein ID
    #        2 - temperature label
    identificator = data[key]['X'][index].name.split('|')[id_index]
    if last_value:
        return identificator
    else:
        return identificator + ', '
        
# A function that processes embeddings to be represented in CSV format
def get_embeddings_tensor_as_CSV(data, embedding_tensor_index, key, last_value=False):
    record = ''
    for j in range(1280):
        embeddings_element = f"{data[key][embedding_tensor_index][j].item():{6}.{3}}"
        record = record + embeddings_element

        if j == 1279 and not last_value:
            record = record + ', '
        elif j == 1279 and last_value:
            record = record 
        else:
            record = record + ', '

    return record

# A function that processes temperature labels to be represented in CSV format
def get_temperature_label_as_CSV(data, embedding_tensor_index, key, last_value=True):
    temperature_label = str(data[key][embedding_tensor_index].item())
    if last_value:
        return temperature_label
    else:
        return temperature_label + ', '

# A function that calculates Matthew's correlation coefficient
def calculate_MCC(predictions_file_name, true_labels_index, prediction_index, separator="\t", has_header=True):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    counter = 0
    with open(predictions_file_name) as file:
        predictions_file = csv.reader(file, delimiter=separator)
        for line in predictions_file:
            if counter > 0:
                if float(line[true_labels_index]) >= 0.65 and float(line[prediction_index]) >= 0.5:
                    TP += 1
                if float(line[true_labels_index]) < 0.65 and float(line[prediction_index]) < 0.5:
                    TN += 1
                if float(line[true_labels_index]) < 0.65 and float(line[prediction_index]) >= 0.5:
                    FP += 1
                if float(line[true_labels_index]) >= 0.65 and float(line[prediction_index]) < 0.5:
                    FN += 1 
            counter = counter + 1
    file.close()
    MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
    return MCC
