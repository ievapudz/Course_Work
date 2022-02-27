#!/usr/bin/env python3.7

# A script that calculates accuracy of predictions in respect
# of each organism determined by TaxID.

# Input: predictions TSV or CSV file.
# Output: percentage of correctly predicted temperature classes.

# Call:
# ./scripts/003/003_accuracy_per_organism.py results/SLP/003/testing_v2_predictions.tsv results/SLP/003/testing_v2_accuracy_per_taxid.tsv

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import return_SV_as_dict
from model_flow import calculate_accuracy_per_tax_id

predictions_file_name = sys.argv[1]
out_file_name = sys.argv[2]

SV_contents =  return_SV_as_dict(predictions_file_name, 0, 2, 3, 
                                 separator="\t", has_header=False,
                                 threshold=0.5)

calculate_accuracy_per_tax_id(SV_contents, out_file_name)
