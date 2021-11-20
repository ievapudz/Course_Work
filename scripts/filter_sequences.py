"""
This module contains a function that filters sequences based on whether they have
embeddings or not. The lists of sequences with embeddings for each dataset are placed
in ./data/EMB_ESM1b directory with a file extension `.lst`.
"""

def filter_sequences_with_embeddings(data):
    data_filtered = {
        'train': {
            'X': [],
            'Y': [],
            'FASTA_prefix': 'data/FASTA/filtered_training_',
            'CSV_prefix': 'data/CSV/filtered_training_',
            'embedding_list': './data/EMB_ESM1b/training_embeddings_sample.lst',
            'embeddings': 'training_embeddings_sample'
        },
        'validate': {
            'X': [],
            'Y': [],
            'FASTA_prefix': 'data/FASTA/filtered_validation_',
            'CSV_prefix': 'data/CSV/filtered_validation_',
            'embedding_list': './data/EMB_ESM1b/validation_embeddings.lst',
            'embeddings': '/content/drive/MyDrive/validation_sequences'
        },
        'test': {
            'X' : [],
            'Y' : [],
            'FASTA_prefix': 'data/FASTA/filtered_testing_',
            'CSV_prefix': 'data/CSV/filtered_testing_',
            'embedding_list': './data/EMB_ESM1b/testing_embeddings.lst',
            'embeddings': '/content/drive/MyDrive/testing_sequences'
        }
    }

    for element in data.keys():
        emb_list_handle = open(data_filtered[element]['embedding_list'], 'r')
        emb_list = emb_list_handle.readlines()
        emb_list_handle.close()
        emb_set = set()
        for j in range(len(emb_list)):
            emb_set.add(emb_list[j].split('.')[0])
        for i in range(len(data[element]['X'])):
            if(data[element]['X'][i].id.split('|')[1] in emb_set):
                data_filtered[element]['X'].append(data[element]['X'][i])
                data_filtered[element]['Y'].append(data[element]['Y'][i])
