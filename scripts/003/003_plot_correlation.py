#!/usr/bin/env python3.7

import matplotlib.pyplot as plt
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1], sep="\t")
df.plot(
    xlabel='x',
    ylabel='y',
    title='True temperature VS predicted temperature'
)

plt.savefig(sys.argv[2])
