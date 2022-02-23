#!/usr/bin/env python3.7

import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy
from kern_smooth import densCols
from matplotlib import cm

df = pd.read_csv(sys.argv[1], sep="\t")

x = df['temperature']
y = df['prediction']

densities = densCols(x, y, nbin = 128)
#plt.scatter(x, y, c='navy')
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
