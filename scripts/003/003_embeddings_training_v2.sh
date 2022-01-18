#!/bin/bash

# It is a submission script to run embeddings
# generation program.

set -ue

#SBATCH --job-name=003_training_v2
#SBATCH --output=data/003/slurm/training.out

#SBATCH --ntasks=30
#SBATCH --mem-per-cpu=8000

DATA_DIR=data/003/
JOB_NAME=training_v2
FASTA_PREFIX=${DATA_DIR}FASTA/${JOB_NAME}/${JOB_NAME}.part-

echo "Job started at $(date)"

for((i = 1 ; i < 31 ; i++));
do
    srun --ntasks 1 python3.7 ../programs/esm-0.4.0/extract.py esm1b_t33_650M_UR50S ${FASTA_PREFIX}${i}.fasta ${DATA_DIR}EMB_ESM1b/${JOB_NAME}/ --repr_layers 0 32 33 --include mean per_tok
done

echo "Job end at $(date)"

