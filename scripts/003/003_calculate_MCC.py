#!/usr/bin/env python3.7

# A script that is used to calculate Matthew's correlation coefficient

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file_actions import calculate_MCC

predictions_file_name = sys.argv[1]
print('MCC: '+str(calculate_MCC(predictions_file_name, 0, 1)))

