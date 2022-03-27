#!/usr/bin/env python3.7

# A script that analyses the contents of per_tok embedding

import sys
import torch

from data_process import create_testing_data
from data_process import filter_sequences
from data_process import get_ESM_embeddings_as_tensor
from data_process import save_tensors_as_NPZ
from data_process import print_tensors_as_SV_to_file

per_tok_PT = sys.argv[1]
fasta_file = sys.argv[2]
emb_dir = sys.argv[3]

per_tok_embedding = torch.load(per_tok_PT)

#print(per_tok_embedding['representations'][33], len(per_tok_embedding['representations'][33]))

data = create_testing_data(fasta_file, emb_dir, emb_case=1, labelled=False)

filter_sequences(data, 'test', data['test']['embeddings'], labelled=False)

[Xs_input_tensor, Ys_input_tensor] = get_ESM_embeddings_as_tensor(data, ['test'], emb_key='representations')

print("Saving tensors to NPZ file")
save_tensors_as_NPZ([Xs_input_tensor, Ys_input_tensor],
				['x_input', 'y_input'],
				emb_dir+fasta_file+'.npz')

input_tensor = { 'x_input': Xs_input_tensor, 'y_input': Ys_input_tensor }

print("Saving tensors to a TSV file")
print_tensors_as_SV_to_file(data, input_tensor, 'test', ['x_input', 'y_input'],
						out_file_name=emb_dir+fasta_file+'.tsv',
						sep="\t", labelled=False)
