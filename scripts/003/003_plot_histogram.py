#!/usr/bin/env python3.7

# A script that plots data distribution histogram. 

# An example usage:
# ./scripts/003/003_plot_histogram.py data/003/TSV/training_v2_tensors.tsv 3 data/003/visualisation_v2/training_v2_histo.png

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import matplotlib.pyplot as plt

DATA_FILE = sys.argv[1]
COL_INDEX = int(sys.argv[2])
OUT_FILE = sys.argv[3]

# Read data file

file_handle = open(DATA_FILE, 'r')

temperatures = []
 
while True: 
	# Get next line from file
	line = file_handle.readline()
 
	# if line is empty
	# end of file is reached
	if not line:
		break
	
	temperatures.append(int(line.split('\t')[COL_INDEX]))
 
file_handle.close()

# Plot histogram

n, bins, patches = plt.hist(x=temperatures, bins=10, color='#00008b')
plt.xticks(range(0, 110, 10))
plt.yticks(range(0, 85000, 5000))
plt.xlabel('temperature')
plt.ylabel('number of proteins')

if(len(sys.argv) >= 5 and sys.argv[4]):
	plt.title(sys.argv[4]+' sequences distribution histogram')
else:
	plt.title('Sequences distribution histogram')

plt.savefig(OUT_FILE)
