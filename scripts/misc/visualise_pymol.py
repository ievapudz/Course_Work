#!/usr/bin/env python3.7

# A script that automatically visualises pairs of proteins

import sys
import os

pdb_file_1 = sys.argv[1]
pdb_file_2 = sys.argv[2]
png_file_dir = sys.argv[3]

pdb_id_1 = os.path.splitext(pdb_file_1)[0].split('/')[-1]
pdb_id_2 = os.path.splitext(pdb_file_2)[0].split('/')[-1]

cline = f'load {pdb_file_1}, {pdb_id_1}\nload {pdb_file_2}, {pdb_id_2}\n'+\
        f'spectrum b, selection=all\nalign {pdb_id_1}, {pdb_id_2}\n'+\
        f'png {png_file_dir}/{pdb_id_1}_{pdb_id_2}.png\n'+\
        f'hide all\n'+\
        f'show cartoon, {pdb_id_1}\npng {png_file_dir}/{pdb_id_1}.png\n'+\
        f'hide all\n'+\
        f'show cartoon, {pdb_id_2}\npng {png_file_dir}/{pdb_id_2}.png\n'+\
        f'quit\n'

pml_file = pdb_id_1+'_'+pdb_id_2+'.pml'

file_handle = open(pml_file, 'w')

file_handle.write(cline)

file_handle.close()

os.system(f'pymol -Q -W 0 {pml_file}')
os.system(f'rm {pml_file}')


