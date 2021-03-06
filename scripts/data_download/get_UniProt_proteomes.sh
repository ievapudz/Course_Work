#!/bin/bash

set -ue

# A script to get proteomes based on UniParc identifier
# Example usage:
# ./scripts/data_download/get_UniProt_proteomes.sh data/003/003.tsv 0

DATASET_FILE=$1
INITIAL_INDEX=$2

NAMES=($(cat ${DATASET_FILE} | awk '{ print $1 }'))
UP_IDS=($(cat ${DATASET_FILE} | awk '{ print $2 }'))

for((i = "${INITIAL_INDEX}" ; i < "${#UP_IDS[@]}" ; i++));
do
    echo "$i/${#UP_IDS[@]}: downloading ${UP_IDS[$i]}"
    PROTEOME_URL="https://www.uniprot.org/uniprot/?query=proteome:"${UP_IDS[$i]}"&format=fasta"
    PROTEOME_FASTA="data/003/FASTA/"${NAMES[$i]}".fasta"
    curl -s ${PROTEOME_URL} > ${PROTEOME_FASTA} 
done