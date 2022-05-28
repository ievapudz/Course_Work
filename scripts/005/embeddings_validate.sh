#!/bin/bash

# It is a submission script to run embeddings
# generation program.

set -ue

#SBATCH --job-name=005_validation
#SBATCH --output=data/005/slurm/validation.out

#SBATCH --nodes=7
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=8000

DATA_DIR=data/005/
JOB_NAME=validate
FASTA_PREFIX=${DATA_DIR}FASTA/${JOB_NAME}/${JOB_NAME}_

echo "Job started at $(date)"

srun --ntasks 1 python3.7 ../programs/esm-0.4.0/extract.py esm1b_t33_650M_UR50S\
	${FASTA_PREFIX}${SLURM_ARRAY_TASK_ID}.fasta ${DATA_DIR}EMB_ESM1b/${JOB_NAME}/\
	 --repr_layers 33 --include mean 

echo "Job end at $(date)"

