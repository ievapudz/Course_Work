#!/usr/bin/env python3.7

import matplotlib.pyplot as plt
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], sep="\t")

x = df['temperature']
y = df['prediction']

plt.scatter(y, x)
plt.title('A plot to show the correlation between temperature and prediction')
plt.xlabel('Normalised temperature')
plt.ylabel('Prediction value')
plt.plot()
plt.savefig(sys.argv[2])
