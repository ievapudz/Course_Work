#!/usr/bin/env python3.7

# A script that tests plot_prediction function

# Example usage:
# ./plot_predictions.py predictions/0330_per_tok.tsv predictions/0330_per_tok.png

import sys
from results import plot_predictions

predictions_file = sys.argv[1]
predictions_plot_file = sys.argv[2]

plot_predictions(predictions_file, 'Cas13X.1', [1, 4], '\t', predictions_plot_file)
