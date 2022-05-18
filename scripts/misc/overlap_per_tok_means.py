#!/usr/bin/env python3.7

# A script that finds the overlap between two sequences in files with headers
# and calculates means for each overlap.

# Example usage:
# ./scripts/misc/overlap_per_tok_means.py predictions/TSV/Cas12a_1022_splits.part-1.per_tok.tsv predictions/TSV/Cas12a_N_per_tok_1.tsv 4 4 N 

import sys
from statistics import mean

sequences = {}

file_1 = sys.argv[1]
file_2 = sys.argv[2]
index_1 = int(sys.argv[3])
index_2 = int(sys.argv[4])
term = sys.argv[5]

file_handle = open(file_1, 'r')
lines_1 = file_handle.readlines()[1:]
file_handle.close()

for line in lines_1:
	line = line.rstrip()
	seq_id = line.split('\t')[0]
	if(seq_id not in sequences):
		sequences[seq_id] = {}
		sequences[seq_id]['0'] = []
		sequences[seq_id]['1'] = []
	prediction = float(line.split('\t')[index_1])
	
	sequences[seq_id]['0'].append(prediction)

file_handle = open(file_2, 'r')
lines_2 = file_handle.readlines()[1:]
file_handle.close()

for line in lines_2:
	line = line.rstrip()
	seq_id = line.split('\t')[0]
	prediction = float(line.split('\t')[index_2])
	sequences[seq_id]['1'].append(prediction)

if(term == 'N'):
	for seq_id in list(sequences.keys()):
		overlap_length = min([len(sequences[seq_id]['0']), 
								len(sequences[seq_id]['1'])])
		if(overlap_length):
			mean_1 = mean(sequences[seq_id]['0'][0:overlap_length])
			mean_2 = mean(sequences[seq_id]['1'][0:overlap_length])
			print(seq_id, '\t', mean_1, '\t', mean_2, '\t', mean_1-mean_2)
elif(term == 'C'):
	for seq_id in list(sequences.keys()):
		overlap_length = min([len(sequences[seq_id]['0']), 
								len(sequences[seq_id]['1'])])
		if(overlap_length):
			mean_1 = mean(sequences[seq_id]['0'][len(sequences[seq_id]['0'])-overlap_length:])
			mean_2 = mean(sequences[seq_id]['1'][len(sequences[seq_id]['1'])-overlap_length:])
			print(seq_id, '\t', mean_1, '\t', mean_2, '\t', mean_1-mean_2)
