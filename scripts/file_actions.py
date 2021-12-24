import os
import numpy
import pymde
import torch
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

def load_tensor_data_from_NPZ(NPZ_file_name, data_subset_keyword):
    # This function loads Tensor data from the specified NPZ file
    with numpy.load(NPZ_file_name) as data_loaded:
        data_subset = data_loaded[data_subset_keyword]
    data_subset_tensor = torch.from_numpy(data_subset)
    return data_subset_tensor