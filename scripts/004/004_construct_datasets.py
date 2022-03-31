#!/usr/bin/env python3.7

# A script that constructs 004 dataset.

# Example usage:
# ./scripts/004/004_construct_datasets.py data/003/FASTA/

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from dataset_processing import fill_model_sets
from dataset_processing import get_list_of_proteomes
from dataset_processing import filter_sequences_by_length_before_embeddings
from file_actions import print_SeqRecords_to_FASTA 

proteome_directory = sys.argv[1]
sets_directory = sys.argv[2]

seqs_in_set = 10000

ranges = [ '^([0-9]_.*|(1[0-4])_.*)_.*$', 
		   '^1[5-9]_.*', 
		   '^2[0-4]_.*', '^2[5-9]_.*', 
		   '^3[0-4]_.*', '^3[5-9]_.*',
		   '^4[0-4]_.*', '^4[5-9]_.*', 
		   '^5[0-4]_.*', '^5[5-9]_.*',
		   '^6[0-4]_.*', '^6[5-9]_.*', 
		   '^7[0-4]_.*', '^7[5-9]_.*',
		   '^8[0-4]_.*', 
		   '^(8[5-9]_.*|(9[0-9])_.*|100_.*)_.*$' ]

max_seq_in_prots = 800

sets = {}

for range_regex in ranges:
	proteomes = get_list_of_proteomes(proteome_directory, range_regex)
	filtered_sequences = filter_sequences_by_length_before_embeddings(proteomes, proteome_directory, 1022)
	
	one_range_sets = fill_model_sets(proteomes, filtered_sequences, range_regex, max_seq_in_prots, seqs_in_set,
					[0.7, 0.15, 0.15], 1022)

	sets[range_regex] = one_range_sets

for i, range_regex in enumerate(ranges):
	for set_name in ['train', 'validate', 'test']:
		print_SeqRecords_to_FASTA(sets[ranges[i]][set_name], sets_directory+'/'+\
								  set_name+'_'+str(i)+'.fasta')
