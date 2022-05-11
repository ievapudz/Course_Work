#!/usr/bin/env python3.7

# A script that draws a plot for data dots
# from a single file (TSV)

import os
import sys
import matplotlib.pyplot as plt

data_file = sys.argv[1]
x_index = int(sys.argv[2])
y_indeces = list(map(int, sys.argv[3:]))

file_handle = open(data_file, "r")
lines = file_handle.readlines()[1:]
file_handle.close()

x = []
y = []
for y_index in y_indeces[0:1]:
	for line in lines:
		#x.append(line.split("\t")[x_index])
		x = range(len(lines))
		y.append(line.split("\t")[y_index])
		y = list(map(float, y))

	plt.scatter(x, y)
	x = []
	y = []

pathname, extension = os.path.splitext(data_file)
plt.savefig(pathname.split('/')[-1]+'.png')

