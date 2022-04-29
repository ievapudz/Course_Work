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
FASTA_PREFIX=Cas12b_C

#FASTA="${DIR}/${FASTA_PREFIX}.part-${SLURM_ARRAY_TASK_ID}.fasta"
#srun ./thermoclass -f "${FASTA}" -g --per_tok -e "emb/${FASTA_PREFIX}/" -t "emb/${FASTA_PREFIX}_per_tok_${SLURM_ARRAY_TASK_ID}.tsv" -n \
#			   "emb/${FASTA_PREFIX}_per_tok_${SLURM_ARRAY_TASK_ID}.npz" -o "predictions/TSV/${FASTA_PREFIX}_per_tok_${SLURM_ARRAY_TASK_ID}.tsv" \
#				--output_fasta "predictions/FASTA/${FASTA_PREFIX}_per_tok_${SLURM_ARRAY_TASK_ID}.fasta" --output_plot \
#			   "predictions/PNG/"

FASTA="${DIR}/${FASTA_PREFIX}.fasta"
srun ./thermoclass -f "${FASTA}" -g --per_tok -e "emb/${FASTA_PREFIX}/" -t "emb/${FASTA_PREFIX}_per_tok.tsv" -n \
			   "emb/${FASTA_PREFIX}_per_tok.npz" -o "predictions/TSV/${FASTA_PREFIX}_per_tok.tsv" \
				--output_fasta "predictions/FASTA/${FASTA_PREFIX}_per_tok.fasta" --output_plot \
			   "predictions/PNG/"
