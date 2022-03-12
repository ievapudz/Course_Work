#!/usr/bin/env python3.7

# A script that calculates aminoacid
# frequency averages for a TSV file,
# where aminoacid frequencies are 
# considered as embeddings.

import os
import sys
import pandas
import matplotlib.pyplot as plt

TSV_file = sys.argv[1]
data = pandas.read_csv(TSV_file, sep='\t', header=None)

data.columns = ['taxid', 'seqid', 'length', 'temperature', 
                'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 
                'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
                'W', 'Y']

class_0_data = data[data.temperature < 65]
class_1_data = data[data.temperature >= 65]

class_means = {}

for i in range(4, len(class_0_data.columns)):
    class_means[class_0_data.columns[i]] = [0, 0]
    class_means[class_0_data.columns[i]][0] = class_0_data[class_0_data.columns[i]].mean()
    class_means[class_1_data.columns[i]][1] = class_1_data[class_1_data.columns[i]].mean()

class_means_df = pandas.DataFrame(class_means)

class_means_df = class_means_df.T

class_means_df.plot.scatter(x=0, y=1)

for i, label in enumerate(data.columns[4:]):
    plt.annotate(label, (class_means_df[0][i], class_means_df[1][i]))

plt.xlabel('Class 0')
plt.ylabel('Class 1')
plt.savefig(sys.argv[2])
