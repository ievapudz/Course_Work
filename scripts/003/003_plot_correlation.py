#!/usr/bin/env python3.7

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
plt.ylim(-2.5, 2.5)
plt.xlim(-2.5, 2.5) 
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
thresholds = [ -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0,
               0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 ]
for threshold in thresholds:
    print('Matthew\'s correlation coefficient (with prediction threshold '+str(threshold)+'): ')
    print(calculate_MCC(x, y, real_threshold=threshold, prediction_threshold=threshold))
    print()
