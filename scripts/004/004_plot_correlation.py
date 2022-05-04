#!/usr/bin/env python3.7

# A script that plots correlation plots for regressor inferences and
# calculates correlation coefficients (Pearson, Spearman and Matthew's).

# An example usage:
# ./scripts/004/004_plot_correlation.py results/regressor/004/testing_predictions.tsv results/regressor/004/testing_predictions.png 0.1 0.9 True

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import matplotlib.pyplot as plt
import pandas as pd
import numpy
from kern_smooth import densCols
from matplotlib import cm
from model_dataset_processing import load_tensor_from_NPZ
from model_dataset_processing import standard_deviation
from model_dataset_processing import convert_z_score_to_label
from results_processing import calculate_MCC

Z_SCORE_NORM = False

if(len(sys.argv) >= 6 and bool(sys.argv[5]) == True):
    Z_SCORE_NORM = bool(sys.argv[5])
    # Loading tensors to get the standard deviation of the dataset
    data_test = load_tensor_from_NPZ(
        'data/003/NPZ/testing_embeddings_v2.npz',
        ['x_test', 'y_test'])

    std = standard_deviation(data_test['y_test'], 65)

df = pd.read_csv(sys.argv[1], sep="\t")

x = df['temperature']
y = df['prediction']

densities = densCols(x, y, nbin = 128)
plt.figure(figsize=(8,6))
plt.title('A plot to show the correlation between temperature and prediction')

maximum = max([max(x), max(y)])
minimum = min([min(x), min(y)])

plt.ylim(minimum, maximum)
plt.xlim(minimum, maximum) 
plt.xlabel('Normalised temperature')
plt.ylabel('Prediction value')
sc = plt.scatter(x, y, c=densities, s=15, edgecolors='none', alpha=0.75, cmap=cm.jet)
plt.colorbar(sc)
plt.show()

m, b = numpy.polyfit(x, y, 1)
plt.plot(x, m*x+b, color='lightpink')

plt.savefig(sys.argv[2])

# Printing Pearson's correlation
print('Pearson\'s correlation: ')
print(df.corr())
print()

# Printing Spearman's correlation
print('Spearman\'s correlation: ')
print(df.corr(method="spearman"))
print()

# Printing Matthew's correlation coefficient
thresholds = numpy.linspace(float(sys.argv[3]), float(sys.argv[4]),
                            int((float(sys.argv[4])-float(sys.argv[3]))/0.1), 
                            False)

for threshold in thresholds:
    converted_threshold = ''
    if(Z_SCORE_NORM):
        converted_threshold = convert_z_score_to_label(threshold, 65, std)
    else:
        converted_threshold = threshold * 100 

    print('Matthew\'s correlation coefficient (with prediction threshold '+\
          str(round(threshold, 2))+' (real: '+str(converted_threshold.item())+')): ')
    print(calculate_MCC(x, y, real_threshold=threshold, 
          prediction_threshold=threshold))
    print()
