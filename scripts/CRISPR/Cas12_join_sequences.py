#!/usr/bin/env python3.7

# A script that joins N and C terms of sequences

import sys
from Bio import SeqIO

N_file = sys.argv[1]
C_file = sys.argv[2]

records = []
for record in SeqIO.parse(N_file, 'fasta'):
	records.append(record)

for record in SeqIO.parse(C_file, 'fasta'):
	for saved_record in records:
		if(saved_record.name == record.name):
			saved_record.seq += record.seq

for record in records:
	print('>'+record.name)
	print(record.seq)

