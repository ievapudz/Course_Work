#!/usr/bin/env python3.7

# A script that plots correlation plots for regressor inferences and
# calculates correlation coefficients (Pearson, Spearman and Matthew's).

# An example usage:
# ./scripts/003/003_plot_correlation.py results/regressor/003/testing_4_real_and_predictions_normalised.tsv results/regressor/003/testing_4_real_vs_predictions_normalised.png 0.3 0.9

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
from results_processing import calculate_MCC

df = pd.read_csv(sys.argv[1], sep="\t")

x = df['temperature']
y = df['prediction']

densities = densCols(x, y, nbin = 128)
plt.figure(figsize=(8,6))
plt.title('A plot to show the correlation between temperature and prediction')
plt.ylim(round(float(sys.argv[3])), round(float(sys.argv[4])))
plt.xlim(round(float(sys.argv[3])), round(float(sys.argv[4]))) 
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
    print('Matthew\'s correlation coefficient (with prediction threshold '+\
          str(round(threshold, 2))+'): ')
    print(calculate_MCC(x, y, real_threshold=threshold, 
          prediction_threshold=threshold))
    print()
