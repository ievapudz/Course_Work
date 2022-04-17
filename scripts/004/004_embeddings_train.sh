#!/bin/bash

# It is a submission script to run embeddings
# generation program.

set -ue

#SBATCH --job-name=004_train
#SBATCH --output=data/004/slurm/train.out

#SBATCH --nodes=7
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=8000

DATA_DIR=data/004/
JOB_NAME=train
FASTA_PREFIX=${DATA_DIR}FASTA/${JOB_NAME}/${JOB_NAME}_

echo "Job started at $(date)"

srun --ntasks 1 python3.7 ../programs/esm-0.4.0/extract.py esm1b_t33_650M_UR50S\
	${FASTA_PREFIX}${SLURM_ARRAY_TASK_ID}.fasta ${DATA_DIR}EMB_ESM1b/${JOB_NAME}/\
	 --repr_layers 33 --include mean 

echo "Job end at $(date)"

