import os
"""
This module contains a function that filters sequences based on whether they have
embeddings or not. 
"""

def filter_sequences(data, key, path_to_embeddings):
    # The function that replaces the filter_sequences_with_embeddings.
    # The functionality stays the same, however new dictionary 'data' is not created.
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