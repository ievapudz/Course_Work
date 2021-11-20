import sys

"""
This module contains functions that are devoted to create FASTA and CSV files out
of information in data dictionary, which is created by data_division function in 
`data_division.py`.
"""

def create_division_FASTA(data):
    for element in data.keys():
        file_name = data[element]['FASTA_prefix']+'sequences.fasta'
        file_handle = open(file_name, 'w')
        for record in data[element]['X']:
            file_handle.write('>'+record.name.split('|')[1])
            file_handle.write("\n")
            file_handle.write(str(record.seq))
            file_handle.write("\n")
        file_handle.close()

def create_division_CSV(data):
    for element in data.keys():
        file_name = data[element]['CSV_prefix']+'temperature_annotations.csv'
        file_handle = open(file_name, 'w')
        file_handle.write('identifier,label'+"\n")
        for i in range(len(data[element]['X'])):
            file_handle.write(data[element]['X'][i].name.split('|')[1]+','+str(data[element]['Y'][i]))
            file_handle.write("\n")
        file_handle.close()
