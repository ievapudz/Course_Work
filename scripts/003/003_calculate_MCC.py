#!/usr/bin/env python3.7

# A script that is used to calculate Matthew's correlation coefficient

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import calculate_MCC
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--predictions', '-p', dest='predictions_file_name',
				   help='path to the TSV file with predictions')

parser.add_option('--header', dest='header', default=False,
				   action='store_true',
				   help='set to determine whether the file has a header')

parser.add_option('--true-label-idx', dest='true_label_index',
				   help='set the index of the true label column')

parser.add_option('--prediction-idx', dest='prediction_index',
				   help='set the index of the prediction column')

parser.add_option('--threshold', dest='threshold',
				   help='set the true label threshold')

(options, args) = parser.parse_args()

print('MCC: '+str(calculate_MCC(options.predictions_file_name, 
	int(options.true_label_index), int(options.prediction_index), 
	has_header=options.header, threshold=float(options.threshold))))

