#!/usr/bin/env python3.7

# A script that turns the predictions of kmers into 
# FASTA sequences (of class labels)

# Usage:
# ./scripts/CRISPR/C2EP_kmers_processing_results.py results/SLP/CRISPR/C2EP_kmers_predictions_sorted.tsv results/SLP/CRISPR/C2EP_kmers_predictions.fasta

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from results_processing import get_kmers_results_as_FASTA

input_file = sys.argv[1]
output_file = sys.argv[2]

get_kmers_results_as_FASTA(input_file, "\t", True, output_file, 
                           include_max=True, include_min=True, 
                           include_mean=True, include_median=True, 
                           include_std=True)
