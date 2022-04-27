#!/usr/bin/env python3.7

# A script that runs PyMOL visualisation for 
# a batch of PDB protein pairs

import sys
import os

firsts = []
seconds = []

for i, arg in enumerate(sys.argv):
    if((i == 0) or (i == len(sys.argv)-1)):
        continue
    elif(i % 2 == 1):
        firsts.append(arg.lower())
    else:
        seconds.append(arg.lower())

png_dir = sys.argv[-1]

if(len(firsts) != len(seconds)):
    print(sys.argv[0]+": inequal number of PDB files to make pairs",
          file=sys.stderr)
    sys.exit(1);

for i in range(len(firsts)):
    cline = f'./scripts/misc/visualise_pymol.py {firsts[i]} {seconds[i]} {png_dir}'
    print(cline)
    os.system(cline)
