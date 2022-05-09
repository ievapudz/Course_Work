#!/usr/bin/env python3.7

# A script that splits sequence into overlapping
# fragments of a certain length

# Usage:
# ./scripts/CRISPR/Cas12_split_to_max_length.py data/CRISPR/FASTA/Cas12a/Cas12a.fasta 1022 

import sys
from Bio import SeqIO

in_file = sys.argv[1]
max_length = int(sys.argv[2])

records = []
for record in SeqIO.parse(in_file, 'fasta'):
	records.append(record)

for record in records:
	if(len(record.seq) > 2*max_length):
		print(sys.argv[0]+': no overlap will be created because sequence is'+\
				'too long.', file=sys.stderr)
		break
	print('>'+record.name+'-1')
	print(str(record.seq)[0:max_length])
	print('>'+record.name+'-2')
	print(str(record.seq)[-max_length:])

