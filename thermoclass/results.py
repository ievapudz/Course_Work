import sys
import statistics
import math
import matplotlib.pyplot as plt

# Preparing kmers results to be printed in FASTA format.
def get_kmers_results_as_FASTA(input_file_name, sep, headerless, output_file_name, indeces,
							   include_min, include_max, include_mean, include_median, include_std):
	# input_file_name 	- [STRING] a separated-value file with binary and raw predictions
	# sep 				- [STRING] a separated-value file separator
	# headerless		- [BOOLEAN] a flag that determines whether a file has got header
	# output_file_name	- [STRING] a name of an output FASTA file
	# indeces			- [LIST] a collection of indeces for data in order: 
	#					  [binary_prediction, raw_prediction] 
	# include_*			- [BOOLEAN] flags that determine which statistics to include

	file_handle = open(input_file_name, 'r')
   
	if(not headerless):
		header = file_handle.readline()
 
	sequences = {} 
	while True:
	
		line = file_handle.readline()
	  
		if not line:
			break
		
		line = line.rstrip()
		line_arr = line.split(sep)
	  
		if(line_arr[0] not in sequences.keys()):
			sequences[line_arr[0]] = {}
			sequences[line_arr[0]]['label_seq'] = line_arr[indeces[0]]
			sequences[line_arr[0]]['predictions'] = []
		else:
			sequences[line_arr[0]]['label_seq'] += line_arr[indeces[0]]
		 
		sequences[line_arr[0]]['predictions'].append(float(line_arr[indeces[1]]))

	file_handle.close()
   
	file_handle = open(output_file_name, 'w')

	for seq in sequences.keys():

	   if(seq == 'Cas'):
		   print(sequences[seq])

	   line_to_write = '>'+seq
	   if(len(sequences[seq]['predictions']) < 2):
		   continue 
	   if(include_min):
		   minimum = min(sequences[seq]['predictions'])
		   line_to_write += "\t"+'min='+str(minimum)
	   if(include_max):
		   maximum = max(sequences[seq]['predictions'])
		   line_to_write += "\t"+'max='+str(maximum)
	   if(include_mean):
		   mean = get_kmers_predictions_mean(sequences, seq)
		   line_to_write += "\t"+'mean='+str(mean)
	   if(include_median):
		   median = statistics.median(sequences[seq]['predictions'])
		   line_to_write += "\t"+'median='+str(median)
	   if(include_std):
		   std = statistics.stdev(sequences[seq]['predictions'])
		   line_to_write += "\t"+'std='+str(std)

	   file_handle.write(line_to_write+"\n"+sequences[seq]['label_seq']+"\n")
	file_handle.close()

# Calculating the average class prediction for the sequence.
def get_kmers_predictions_mean(seq_dict, seq_key):
	predictions_sum = 0

	for pred in seq_dict[seq_key]['predictions']:
		predictions_sum += pred

	mean = predictions_sum / len(seq_dict[seq_key]['label_seq'])

	return mean

# Plotting predictions.
def plot_predictions(predictions_file, seq_key, indeces, sep, output_png, smoothened=False):
	x_values = []
	y_values = []
	file_handle = open(predictions_file, 'r')
	lines = file_handle.readlines()
	file_handle.close()
	for line in lines:
		line_arr = line.split('\t')
		if(line_arr[0] == seq_key):
			x_values.append(int(line_arr[indeces[0]]))
			y_values.append(float(line_arr[indeces[1]]))

	plt.plot(x_values, y_values, linewidth=1, color='black')
	plt.savefig(output_png)
	plt.clf()

