#!/usr/bin/env python3.7

# This is a script that divides given FASTA sequences into sequences
# of length equal to k.

# Example usage:
# ./scripts/CRISPR/C2EP_make_kmers.py data/CRISPR/FASTA/C2EP/C2EP.fasta 1024 data/CRISPR/FASTA/C2EP/C2EP_kmers.fasta

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from kmers import make_kmers
from file_actions import print_SeqRecords_to_FASTA

input_FASTA_file = sys.argv[1]
k = sys.argv[2]
output_FASTA_file = sys.argv[3]

kmers = make_kmers(k, input_FASTA_file)
print_SeqRecords_to_FASTA(kmers, output_FASTA_file) 
