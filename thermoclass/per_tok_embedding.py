#!/usr/bin/env python3.7

# A script that analyses the contents of per_tok embedding

import sys
import torch

per_tok_PT = sys.argv[1]

per_tok_embedding = torch.load(per_tok_PT)

print(per_tok_embedding['representations'][0], len(per_tok_embedding['representations'][0]))
print(per_tok_embedding['representations'][32], len(per_tok_embedding['representations'][32]))
print(per_tok_embedding['representations'][33], len(per_tok_embedding['representations'][33]))
