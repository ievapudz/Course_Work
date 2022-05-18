#!/usr/bin/env python3.7

# A script that merges two files based on the values on one column

import sys

files = []

# indeces list saves indeces of predictions to merge from respective files
indeces = []

# ADD: options parsing should be smarter (more flexible)
for i in range(len(sys.argv)):
	if(i):
		if(i % 2 == 1):
			files.append(sys.argv[i])
		else:
			indeces.append(int(sys.argv[i]))

merged_data = {}

for i, file in enumerate(files):
	file_handle = open(file, 'r')
	lines = file_handle.readlines()[1:]
	for line in lines:
		seq_id = line.strip().split('\t')[0]
		if(seq_id in merged_data.keys()):
			merged_data[seq_id].append(line.strip().split('\t')[indeces[i]])
			merged_data[seq_id].append(str(abs(float(merged_data[seq_id][1])-float(merged_data[seq_id][0]))))
		else:
			merged_data[seq_id] = []
			merged_data[seq_id].append(line.strip().split('\t')[indeces[i]])
	file_handle.close()

# Addition of a header was dedicated to the user of the program
#file_handle.write('seq_id\tmean\taveraged_per_tok\tdelta\n')

for seq_id in sorted(merged_data.keys()):
	line = seq_id+'\t'
	for el in merged_data[seq_id]:
		line += el+'\t'
	print(line)
