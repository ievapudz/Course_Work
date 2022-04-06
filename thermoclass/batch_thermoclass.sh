#!/bin/sh

# A script that runs thermoclass program for a bunch of
# input FASTA files.

DIR=$1
FASTA_PREFIX=$2
INITIAL_INDEX=$3
END_INDEX=$4

FASTAS=($(ls "${DIR}" | grep -e "${FASTA_PREFIX}"))

for((i = "${INITIAL_INDEX}"; i <= "${END_INDEX}" ; i++));
do
	FASTA="${DIR}/${FASTA_PREFIX}$i.fasta"
	./thermoclass -f "${FASTA}" -c -p -e "emb/C2EP/" -t "emb/C2EP_per_tok_${i}.tsv" -n \
				"emb/C2EP_per_tok_${i}.npz" -o "predictions/TSV/C2EP_per_tok_${i}.tsv" \
				 --output_fasta "predictions/FASTA/C2EP_per_tok_${i}.fasta" --output_plot \
				"predictions/PNG/"
done
