#!/usr/bin/env python3.7

# This is a script that generates vectors composed of 20 numbers that
# note the relative frequency of each type aminoacid in the sequence.

import sys
import os
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

FASTA_file = sys.argv[1]

def read_FASTA_sequences(FASTA_file):
    records = []
    for record in SeqIO.parse(FASTA_file, 'fasta'):
        records.append(record)
    return records

records = read_FASTA_sequences(FASTA_file)

for record in records:
    analysed_seq = ProteinAnalysis(str(record.seq))
    print(analysed_seq.get_amino_acids_percent())
