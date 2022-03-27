#!/usr/bin/env python3.7

# A script that analyses the contents of per_tok embedding

import os
import sys
import torch

from data_process import create_testing_data
from data_process import filter_sequences
from data_process import get_ESM_embeddings_as_tensor
from data_process import save_tensors_as_NPZ
from data_process import print_tensors_as_SV_to_file
from inference import load_tensor_from_NPZ
from inference import unlabelled_test_epoch
from models import SLP_with_sigmoid

from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

fasta_file = sys.argv[1]
emb_dir = sys.argv[2]

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

dataset = load_tensor_from_NPZ(emb_dir+fasta_file+'.npz',
                               ['x_input', 'y_input'])

input_dataset = TensorDataset(dataset['x_input'], dataset['y_input'])
input_loader = DataLoader(input_dataset, shuffle=False)

MODEL='SLP_003.pt'

# Load the trained SLP
model = SLP_with_sigmoid()
model.load_state_dict(torch.load(MODEL))
model.eval()

print('Inference process begins')

unlabelled_test_epoch(model, input_loader, 0.5,
                      file_for_predictions=fasta_file+'_predictions.tsv',
                      binary_predictions_only=False)

print('Inference process has finished')

os.system('echo "thermoclass finished:" `date`')
