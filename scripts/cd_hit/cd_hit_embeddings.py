#!/usr/bin/env python3.7

import sys
from Bio import SeqIO

input_FASTA = sys.argv[1]

class_0 = {}
class_1 = {}

# A function that fills up dictionaries of classes if according records
def sort_FASTA(file_name, class_0, class_1):
    for record in SeqIO.parse(file_name, 'fasta'):
        header_arr = record.name.split('|')
        if(int(header_arr[2]) >= 65):
            if header_arr[0] not in class_1:
                class_1[header_arr[0]] = []
            class_1[header_arr[0]].append(record)
        else:
            if header_arr[0] not in class_0:
                class_0[header_arr[0]] = []
            class_0[header_arr[0]].append(record)     

sort_FASTA(input_FASTA, class_0, class_1)

class_0_keys_sorted = sorted(class_0.keys())

# Class 0 proteomes for 004 training
for i in range(32):
    for record in class_0[class_0_keys_sorted[i]]:
        print(record.name)

# Class 0 proteomes for 004 validation
for i in range(33, 40):
    for record in class_0[class_0_keys_sorted[i]]:
        print(record.name)

# Class 0 proteomes for 004 testing
for i in range(40, 51):
    for record in class_0[class_0_keys_sorted[i]]:
        print(record.name)

class_1_keys_sorted = sorted(class_1.keys())

# Class 1 proteomes for 004 training
for i in range(77):
    for record in class_1[class_1_keys_sorted[i]]:
        print(record.name)

# Class 1 proteomes for 004 validation
for i in range(77, 94):
    for record in class_1[class_1_keys_sorted[i]]:
        print(record.name)

# Class 1 proteomes for 004 testing
for i in range(94, 111):
    for record in class_1[class_1_keys_sorted[i]]:
        print(record.name)

# Need to collect embeddings from according sets
