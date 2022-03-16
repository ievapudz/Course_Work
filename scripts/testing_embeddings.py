#!/usr/bin/env python3.7

# A script that saves sequences (testing) embeddings to
# NPZ and TSV files.
# It has to be run after embeddings were generated.

# Example usage:
# ./testing_embeddings.py -f data/CRISPR/FASTA/C2EP_kmers_600/C2EP_kmers_600.fasta 
# -e data/CRISPR/EMB_ESM1b/C2EP_kmers_600/ -o data/CRISPR/C2EP_kmers_600

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from optparse import OptionParser
from file_actions import print_tensors_as_SV_to_file
from file_actions import save_tensors_as_NPZ
from dataset_processing import create_testing_data_2
from dataset_processing import filter_sequences
from dataset_processing import get_ESM_embeddings_as_tensor

parser = OptionParser()
parser.add_option("--fasta", "-f", dest="fasta", 
                   help="path to the FASTA of dataset")

parser.add_option("--embeddings", "-e", dest="embeddings",
                   help="path to the embeddings directory")

parser.add_option("--labelled", "-l", dest="labelled",
                   help="flag that determines whether data is labelled")

parser.add_option("--output", "-o", dest="output",
                   help="output prefix (without extension)")

(options, args) = parser.parse_args()

data = create_testing_data_2(options.fasta, options.embeddings, options.labelled)

filter_sequences(data, 'test', data['test']['embeddings'], options.labelled)

[Xs_test_tensor, Ys_test_tensor] = get_ESM_embeddings_as_tensor(data, ['test'])

save_tensors_as_NPZ([Xs_test_tensor, Ys_test_tensor], ['x_test', 'y_test'], 
                    options.output+'.npz')

data_tensor = { 'x_test': Xs_test_tensor, 'y_test': Ys_test_tensor }

print_tensors_as_SV_to_file(data, data_tensor, 'test',  ['x_test', 'y_test'],
                                dim=1280, subkey='X_filtered', out_file_name=options.output+'.tsv',
                                sep='\t', labelled=options.labelled)
