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
	#		those FASTA records should have the temperature label in their headers.
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
	with numpy.load(NPZ_file_name, allow_pickle=True) as data_loaded:
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

# Printing tensors to *SV file
def print_tensors_as_SV_to_file(data, data_tensor, key_data, keys_tensor, 
								dim=1280, subkey='X_filtered', out_file_name='', 
								sep=',', labelled=True):
	file_handle = open(out_file_name, "w")
	for i in range(len(data_tensor[keys_tensor[0]])):
		if(labelled):
			record = get_id_as_CSV(data, i, key_data, 0, subkey=subkey, sep=sep) + \
					 get_id_as_CSV(data, i, key_data, 1, subkey=subkey, sep=sep) + \
					 get_sequence_length_as_CSV(data, i, key_data, subkey=subkey, 
												sep=sep) + \
					 get_temperature_label_as_CSV(data_tensor, i, 
												  keys_tensor[1], 
												  sep=sep, last_value=False) + \
					 get_embeddings_tensor_as_CSV(data_tensor, i, 
												  keys_tensor[0], dim=dim,
												  sep=sep, last_value=True)
		else:
			record = data[key_data][subkey][i].name + sep + \
					 data[key_data][subkey][i].seq + sep + \
					 get_sequence_length_as_CSV(data, i, key_data, subkey=subkey, sep=sep) + \
					 get_embeddings_tensor_as_CSV(data_tensor, i, keys_tensor[0], 
												  dim=dim, sep=sep, last_value=True)
		file_handle.write(str(record)+"\n")
 
	file_handle.close()

# A function that prints embedding with its temperature label as CSV
def print_tensor_as_CSV(data, data_tensor, key_data, keys_tensor, 
						sep=',', labelled=True):
	# data - a dictionary that contains keys for which values are embeddings and temperature label
	# keys - an array with a key pair: ['x_set', 'y_set']
	file_handle = None

	if(file_name != ''):
		file_handle = open(file_name, 'w')

	for i in range(len(data_tensor[keys_tensor[0]])):
		if(labelled):
			record = get_id_as_CSV(data, i, key_data, 0, sep) + \
					 get_id_as_CSV(data, i, key_data, 1, sep) + \
					 get_sequence_length_as_CSV(data, i, key_data, sep) + \
					 get_temperature_label_as_CSV(data_tensor, i, 
												  keys_tensor[1], sep,
												  False) + \
					 get_embeddings_tensor_as_CSV(data_tensor, i, 
												  keys_tensor[0], True)
		else:
			record = data[key_data]['X_filtered'][i].name + sep + \
					 data[key_data]['X_filtered'][i].seq + sep + \
					 get_sequence_length_as_CSV(data, i, key_data, sep) + \
					 get_embeddings_tensor_as_CSV(data_tensor, i, keys_tensor[0], 
												  sep, True)
		if(file_name == ''):
			print(record)
		else:
			file_handle.write(record+'\n')

	if(file_name != ''):
		file_handle = close()

def print_joined_tensor_as_CSV(data, data_tensor, key_data, keys_tensor, sep=',', labelled=True):
	# data - an array that contains dictionaries with keys, for which values are 
	#		embeddings and temperature label
	for i in range(len(data_tensor[keys_tensor[0]])):
		length = get_joined_sequence_length_as_CSV(data, i, key_data, sep)
		if(labelled):
			record = get_id_as_CSV(data[0], i, key_data, 0, sep) + \
					 get_id_as_CSV(data[0], i, key_data, 1, sep) + length + \
					 get_temperature_label_as_CSV(data_tensor, i,
												  keys_tensor[1], sep,
												  False) + \
					 get_embeddings_tensor_as_CSV(data_tensor, i,
												  keys_tensor[0], True)
		else:
			record = data[0][key_data]['X_filtered'][i].name + sep + \
					 get_sequence_as_CSV(data, i, key_data, sep) + length + \
					 get_embeddings_tensor_as_CSV(data_tensor, i, keys_tensor[0],
												  sep, True)			 
		print(record)
   
# Joining the sequence 
def get_sequence_as_CSV(data, index, key, sep=',', last_value=False):
	# data - an array with objects with sequences in FASTA format
	# index - the index of record in data object
	# key - the chosen key of an inside of data object
	sequence = ''
	for i in range(len(data)):
		sequence += data[i][key]['X_filtered'][index].seq

	if last_value:
		return sequence
	else:
		return sequence + sep


# A function that returns the sequence length for CSV
def get_sequence_length_as_CSV(data, index, key, subkey='X_filtered', 
							   sep=',', last_value=False):
	# data - an object with sequences in FASTA format
	# index - the index of record in data object
	# key - the chosen key of an inside of data object
	sequence_length = str(len(data[key][subkey][index].seq))
	if last_value:
		return sequence_length
	else:
		return sequence_length + sep

# A function that returns the joined sequence length for CSV
def get_joined_sequence_length_as_CSV(data, index, key, subkey='X_filtered',
									  sep=',', last_value=False):
	# data - an array with objects with sequences in FASTA format
	# index - the index of record in data object
	# key - the chosen key of an inside of data object
	sequence_length = 0
	for i in range(len(data)):
		sequence_length += len(data[i][key][subkey][index].seq)

	if last_value:
		return str(sequence_length)
	else:
		return str(sequence_length) + sep

# A function that returns the needed identificator (property) of the sequence
# from the header
def get_id_as_CSV(data, index, key, id_index, subkey='X_filtered', sep=',', last_value=False):
	# data - an object with sequences in FASTA format
	# index - the index of record in data object
	# key - the chosen key of an inside of data object
	# id_index - index that determines which part of FASTA header is taken 
	#		0 - taxonomy ID
	#		1 - protein ID
	#		2 - temperature label
	identificator = data[key][subkey][index].name.split('|')[id_index]
	
	if last_value:
		return identificator
	else:
		return identificator + sep
		
# A function that processes embeddings to be represented in CSV format
def get_embeddings_tensor_as_CSV(data, embedding_tensor_index, key, dim=1280, sep=',', 
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

# A function that processes temperature labels to be represented in CSV format
def get_temperature_label_as_CSV(data, embedding_tensor_index, key, 
							 sep, last_value=True):
	temperature_label = str(data[key][embedding_tensor_index].item())
	
	if last_value:
		return temperature_label
	else:
		return temperature_label + sep

# A function that calculates Matthew's correlation coefficient
def calculate_MCC(predictions_file_name, true_labels_index, prediction_index, 
				  separator="\t", threshold=65, has_header=True):
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	counter = 0
	with open(predictions_file_name) as file:
		predictions_file = csv.reader(file, delimiter=separator)
		for line in predictions_file:
			if counter > 0:
				if float(line[true_labels_index]) >= threshold and \
					float(line[prediction_index]) >= 0.5:
					TP += 1
				if float(line[true_labels_index]) < threshold and \
					float(line[prediction_index]) < 0.5:
					TN += 1
				if float(line[true_labels_index]) < threshold and \
					float(line[prediction_index]) >= 0.5:
					FP += 1
				if float(line[true_labels_index]) >= threshold and \
					float(line[prediction_index]) < 0.5:
					FN += 1 
			counter = counter + 1
	file.close()
	MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
	return MCC

# Parsing predictions *SV file and returning its contents as dictionary 
def return_SV_as_dict(predictions_file_name, tax_id_index, true_temperature_index, prediction_index, 
					  separator="\t", has_header=True, threshold=0.5):
	contents = {}
	with open(predictions_file_name) as file:
		predictions_file = csv.reader(file, delimiter=separator)
		for index, line in enumerate(predictions_file):
			if(index == 0 and has_header):
				continue
			if(line[tax_id_index] not in contents):
				contents[line[tax_id_index]] = {'0': 0, '1': 0, 'true_temperature': line[true_temperature_index]}
			if(float(line[prediction_index]) < threshold):
				contents[line[tax_id_index]]['0'] += 1
			elif(float(line[prediction_index]) >= threshold):
				contents[line[tax_id_index]]['1'] += 1

	file.close()
	return contents 

# Printing FASTA records given in array of SeqRecords (Biopython objects)
def print_SeqRecords_to_FASTA(seq_records, out_filename):
	file_handle = open(out_filename, 'w')
	for record in seq_records:
		file_handle.write('>'+record.id+"\n"+str(record.seq)+"\n\n")
	file_handle.close()

# Reading mapping from a TSV file into dictionary
def read_map_from_SV(SV_filename, sep="\t", headerless=True):
	mapping = {}
	file_handle = open(SV_filename, 'r')
	lines = file_handle.readlines()
	file_handle.close()
	for line in lines:
		if(line.split(sep)[0] not in mapping.keys()):
			mapping[line.split(sep)[0]] = line.split(sep)[1].strip('\n')
	return mapping

# Reading particular values from file
def get_values_from_SV(SV_filename, indeces, sep="\t", headerless=True):
	values = []
	line_count = 0
	file_handle = open(SV_filename, 'r')
	while True:
		next_line = file_handle.readline()
		if not next_line:
			break

		line_count += 1

		if(headerless==False and line_count==1):
			continue

		line = next_line.strip().split(sep)
		line_values = []

		for index in indeces:
			line_values.append(line[index])
		
		values.append(line_values)

	file_handle.close()

	return values

