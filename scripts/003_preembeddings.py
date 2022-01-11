#!/usr/bin/env python3.7

import sys
from Bio import SeqIO
import math
import random

# The function that reads a list of files
def read_file_list(list_file):
    file_handle = open(list_file, 'r')
    file_list = file_handle.readlines()
    file_handle.close()
    return file_list

# The function that based on the list of files, which names are in format [temperature_label]_[TaxID]_[domain].fasta,
# parses each of the listed FASTA file and classifies its records to classes
def classify_records(file_list, file_prefix, partition=65):
    class_0 = []
    class_1 = []
    for file in file_list:
        [temperature_label, tax_id, domain] = file.split('_')
        for record in SeqIO.parse(file_prefix+file.rstrip(), 'fasta'):
            record.name = tax_id+'|'+record.id.split('|')[1]+'|'+temperature_label
            if(int(temperature_label) >= partition):
                class_1.append(record)
            else:
                class_0.append(record)
    class_0 = random.shuffle(class_0)
    class_1 = random.shuffle(class_1)
    return [class_0, class_1]
    
# The function that writes the needed fraction of an array to the subset file
def write_FASTA(file_name, records_0, records_1, fraction, offset_0, offset_1):
    file_handle = open(file_name, 'w')
    number_of_records_0 = math.floor(len(records_0)*fraction)
    for i in range(offset_0, offset_0+number_of_records_0):
        file_handle.write(records_0[i])
    number_of_records_1 = math.floor(len(records_1)*fraction)
    for i in range(offset_1, offset_1+number_of_records_1):
        file_handle.write(records_1[i])
    file_handle.close()

FASTA_files_prefix = 'data/'

file_list = read_file_list(sys.argv[1])
[class_0, class_1] = classify_records(file_list, sys.argv[2])
write_FASTA(sys.argv[1]+'/training.fasta', class_0, class_1, 0.7, 0)
write_FASTA(sys.argv[1]+'/validation.fasta', class_0, class_1, 0.15, math.floor(len(class_0)*0.7), math.floor(len(class_1)*0.7))
write_FASTA(sys.argv[1]+'/testing.fasta', class_0, class_1, 0.15, math.floor(len(class_0)*0.85), math.floor(len(class_1)*0.85))






