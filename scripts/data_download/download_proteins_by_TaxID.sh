#!/bin/bash

set -ue

# A script to download protein sequences based on taxonomy IDs of organisms

DATASET_FILE=data/002/TSV/validation_temperature_data.tsv
OUT_DIR=data/002/FASTA/validation/

ORGANISM_IDS=($(tail -n +2 ${DATASET_FILE} | awk '{ print $4 }'))

DB='protein'
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

for((i = 0 ; i < "${#ORGANISM_IDS[@]}" ; i++));
#for((i = 10 ; i < 12 ; i++));
do
    ESEARCH_PROTEIN_URL=$BASE"esearch.fcgi?db=protein&term=txid${ORGANISM_IDS[$i]}[Organism:noexp]&usehistory=y"
    PROTEIN_IDS=($(curl ${ESEARCH_PROTEIN_URL} | grep '<Id>' | sed -n 's:.*<Id>\(.*\)</Id>.*:\1:p'))
    if [ "${#PROTEIN_IDS[@]}" != 0 ]
    then
        echo "Downloading: ${PROTEIN_IDS[0]}"
        efetch -db protein -id ${PROTEIN_IDS[0]} -format fasta > ${OUT_DIR}${PROTEIN_IDS[0]}.fasta
    fi
done 
