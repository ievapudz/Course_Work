#!/bin/bash

# It is a submission script to run thermoclass
# per token.

set -ue

#SBATCH --job-name=thermoclass
#SBATCH --output=thermoclass.slurm

#SBATCH --nodes=7
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=8000

DIR=FASTA/
FASTA_PREFIX=C2EP.part-

FASTA="${DIR}/${FASTA_PREFIX}${SLURM_ARRAY_TASK_ID}.fasta"
srun ./thermoclass -f "${FASTA}" -c -p -e "emb/C2EP/" -t "emb/C2EP_per_tok_${SLURM_ARRAY_TASK_ID}.tsv" -n \
               "emb/C2EP_per_tok_${SLURM_ARRAY_TASK_ID}.npz" -o "predictions/TSV/C2EP_per_tok_${SLURM_ARRAY_TASK_ID}.tsv" \
                --output_fasta "predictions/FASTA/C2EP_per_tok_${SLURM_ARRAY_TASK_ID}.fasta" --output_plot \
               "predictions/PNG/"


