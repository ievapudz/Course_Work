#!/usr/bin/env python3.7

import sys
from Bio import SeqIO
import math
import random

# This is a script that divides datasets into training, validation and testing subsets.

# The function that reads FASTA file and saves records as Seq objects
def read_FASTA(file_name):
    FASTA_records = []
    for record in SeqIO.parse(file_name, 'fasta'):
        FASTA_records.append(record)
    #random.shuffle(FASTA_records)
    return FASTA_records
    
# The function that writes the needed fraction of an array to the subset file
def write_FASTA(file_name, records_0, records_1, fraction, offset_0, offset_1):
    file_handle = open(file_name, 'w')
    number_of_records_0 = math.floor(len(records_0)*fraction)
    for i in range(offset_0, offset_0+number_of_records_0):
        file_handle.write('>'+records_0[i].name+"\n")
        file_handle.write(str(records_0[i].seq)+"\n")
    
    number_of_records_1 = math.floor(len(records_1)*fraction)
    for i in range(offset_1, offset_1+number_of_records_1):
        file_handle.write('>'+records_1[i].name+"\n")
        file_handle.write(str(records_1[i].seq)+"\n")
    file_handle.close()

FASTA_files_prefix = sys.argv[1]

print("Reading class 0 file")
class_0 = read_FASTA(FASTA_files_prefix+'/class_0.fasta')
print("Reading class 1 file")
class_1 = read_FASTA(FASTA_files_prefix+'/class_1.fasta')

print("Writing training set")
write_FASTA(FASTA_files_prefix+'/training.fasta', class_0, class_1, 0.7, 0, 0)
print("Writing validation set")
write_FASTA(FASTA_files_prefix+'/validation.fasta', class_0, class_1, 0.15, math.floor(len(class_0)*0.7), math.floor(len(class_1)*0.7))
print("Writing testing set")
write_FASTA(FASTA_files_prefix+'/testing.fasta', class_0, class_1, 0.15, math.floor(len(class_0)*0.85), math.floor(len(class_1)*0.85))






