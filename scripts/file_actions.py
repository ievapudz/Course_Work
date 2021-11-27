import os
from Bio import SeqIO

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
    command = "python3 esm/extract.py "+path_to_esm_extract+" esm1b_t33_650M_UR50S "+path_to_FASTA+" "+path_to_embeddings+" --repr_layers 0 32 33 --include mean per_tok"
    os.system(command)