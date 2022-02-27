#!/usr/bin/env python3.7

# A script that maps the given sets tax IDs to a respective
# domain. The mappings are described in the TSV format.

# Example usage:
# ./scripts/003/003_map_taxid_to_domain.py ./data/003/TSV/all_taxids_domains.tsv ./data/003/TSV/validation_v2_tensors.tsv
# ./scripts/003/003_map_taxid_to_domain.py ./data/003/TSV/all_taxids_domains.tsv ./results/SLP/003/testing_v2_accuracy_per_taxid.tsv

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import read_map_from_SV
from file_actions import get_values_from_SV

taxid_domain_map_file = sys.argv[1]
dataset_TSV_file = sys.argv[2]

mapping = read_map_from_SV(taxid_domain_map_file)

values = get_values_from_SV(dataset_TSV_file, [0, 1, 2, 3], headerless=False)

for index, value_pair in enumerate(values):
    print("\t".join(value_pair), "\t", mapping[value_pair[0]])
    
