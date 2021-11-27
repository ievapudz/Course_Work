#!/usr/bin/env python3.7

import os
from Bio import SeqIO
from sklearn.utils import shuffle
import visualise_embeddings
from visualise_embeddings import visualise_PCA

proteome_files_dir = 'data/proteomes/'

"""
'FASTA_prefix': 'data/FASTA/filtered_training_',
        'embedding_list': './data/EMB_ESM1b/training_embeddings_sample.lst',
        'embeddings': '/content/drive/MyDrive/training_embeddings_sample'
"""

data = {
    '001': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000625_83333', 'UP000000798', 'UP000008183'],
        'temperature_labels': [37, 80, 80],
        'FASTA_prefix': 'data/cluster_tests/001/FASTA/001_',
        'embeddings': 'data/cluster_tests/001/EMB_ESM1b'
    },
    '002': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000077428', 'UP000000792', 'UP000001974_273057'],
        'temperature_labels': [37, 37, 80],
        'FASTA_prefix': 'data/cluster_tests/002/FASTA/002.fasta',
        'embeddings': 'data/cluster_tests/002/EMB_ESM1b/'
    },
    '003': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000798', 'UP000008183', 'UP000001974_273057'],
        'temperature_labels': [37, 37, 37],
        'FASTA_prefix': 'data/cluster_tests/003/FASTA/003.fasta',
        'embeddings': 'data/cluster_tests/003/EMB_ESM1b/'
    },
    '004': {
        'X': [],
        'Y': [],
        'proteomes': ['UP000000625_83333', 'UP000077428', 'UP000000792'],
        'temperature_labels': [80, 80, 80],
        'FASTA_prefix': 'data/cluster_tests/004/FASTA/004.fasta',
        'embeddings': 'data/cluster_tests/004/EMB_ESM1b/'
    }
}

def write_to_file(data, key, X_key, Y_key, headn, file_name, modify_name):
    # modify_name - boolean that determines wehther to add label to the header or not
    file_handle = open(file_name, 'w')
    for i in range(headn):
        if(modify_name):
            file_handle.write(data[key][X_key][i].name+'|'+str(data[key][Y_key][i])+"\n"+str(data[key][X_key][i].seq)+"\n")
        else:
            file_handle.write(data[key][X_key][i].name+"\n"+str(data[key][X_key][i].seq)+"\n")
    file_handle.close()

def parse_proteomes(data, key):
    for i in range(len(data[key]['proteomes'])):
        for record in SeqIO.parse(proteome_files_dir+data[key]['proteomes'][i]+'.fasta', "fasta"):
            processed_record_name = '>'+record.name.split('|')[1]
            record.name = processed_record_name
            data[key]['X'].append(record)
            data[key]['Y'].append(data['001']['temperature_labels'][i])

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

def generate_embeddings(path_to_esm_extract, path_to_FASTA, path_to_embeddings):
    # Required PyTorch
    command = "python3 esm/extract.py "+path_to_esm_extract+" esm1b_t33_650M_UR50S "+path_to_FASTA+" "+path_to_embeddings+" --repr_layers 0 32 33 --include mean per_tok"
    os.system(command)

def filter_sequences(data, key, path_to_embeddings, path_to_FASTA):
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
        if(data[key]['X'][i].id.split('|')[1] in emb_set):
            data[key]['X_filtered'].append(data[key]['X'][i])
            data[key]['Y_filtered'].append(data[key]['Y'][i])

    command = "rm *.tmp"
    os.system(command)


#keys = ['001', '002', '003', '004']
keys = ['001']

for key in keys:
    parse_proteomes(data, key)
    data[key]['X'], data[key]['Y'] = shuffle(data[key]['X'], data[key]['Y'], random_state=1)

    # Checking how many sequences of each class there is in a sample
    print('Number of each class:', data[key]['Y'][0:1000].count(37), data[key]['Y'][0:1000].count(80))

    get_equal_proportions(data, key, 1000, [37, 80])

    # Checking how many sequences of each class there is in a sample
    print('Number of each class (eq):', data[key]['Y_equally_proportioned'][0:1000].count(37), data[key]['Y_equally_proportioned'][0:1000].count(80))

    file_name = 'data/cluster_tests/'+key+'/FASTA/'+key+'.fasta'

    write_to_file(data, key, 'X_equally_proportioned', 'Y_equally_proportioned', 1000, file_name, False)

filter_sequences(data, keys[0], "data/cluster_tests/001/EMB_ESM1b", "data/cluster_tests/001/FASTA/001.fasta")
data['001']['FASTA_prefix'] = 'data/cluster_tests/001/FASTA/001'

visualise_PCA(data, keys, "data/visualisation/001_PCA.png")


