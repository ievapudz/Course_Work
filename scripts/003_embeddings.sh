#!/bin/bash

# It is a submission script to run embeddings
# generation program.

set -ue

#SBATCH --job-name=003_validation_0_999
#SBATCH --output=data/003/slurm/validation_0_999.out

#SBATCH --ntasks=4
#SBATCH --mem-per-cpu=2000
#SBATCH --time=2:00:00

echo "Job started at $(date)"

srun python3.7 ../programs/esm-0.4.0/extract.py esm1b_t33_650M_UR50S data/003/FASTA/validation_0_999.fasta data/003/EMB_ESM1b/validation/ --repr_layers 0 32 33 --include mean per_tok

echo "Job end at $(date)"

