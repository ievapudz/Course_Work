#!/bin/bash

# It is a submission script to run embeddings
# generation program.

set -ue

#SBATCH --job-name=Cas12b_N
#SBATCH --output=data/CRISPR/slurm/Cas12b_N.out

#SBATCH --ntasks=2
#SBATCH --mem-per-cpu=8000

DATA_DIR=data/CRISPR/
JOB_NAME=Cas12b

echo "Job started at $(date)"

srun --ntasks 1 python3.7 ../programs/esm-0.4.0/extract.py esm1b_t33_650M_UR50S \
    ${DATA_DIR}/FASTA/${JOB_NAME}/${JOB_NAME}_N.fasta \
    ${DATA_DIR}EMB_ESM1b/${JOB_NAME}_N/ --repr_layers 0 32 33 --include mean 

echo "Job end at $(date)"

