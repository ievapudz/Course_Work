#!/bin/bash

set -ue

# A script to download protein sequences based on taxonomy IDs of organisms

DATASET_FILE=$1
OUT_DIR=$2
SAMPLE_SIZE=$3

ORGANISM_IDS=($(cat ${DATASET_FILE} | awk '{ print $4 }'))
TEMPERATURES=($(cat ${DATASET_FILE} | awk '{ print $3 }'))

DB='protein'
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

#for((i = 0 ; i < "${#ORGANISM_IDS[@]}" ; i++));
for((i = 0 ; i < "${SAMPLE_SIZE}" ; i++));
do
    ESEARCH_PROTEIN_URL=$BASE"esearch.fcgi?db=protein&term=txid${ORGANISM_IDS[$i]}[Organism:noexp]&usehistory=y"
    PROTEIN_IDS=($(curl ${ESEARCH_PROTEIN_URL} | grep '<Id>' | sed -n 's:.*<Id>\(.*\)</Id>.*:\1:p'))
    if [ "${#PROTEIN_IDS[@]}" != 0 ]
    then
        echo "$i/${#ORGANISM_IDS[@]} Downloading: ${PROTEIN_IDS[0]}"
        ORIG_PROT_FILE=${OUT_DIR}${PROTEIN_IDS[0]}.fasta
        PROT_FILE=${OUT_DIR}${ORGANISM_IDS[$i]}.fasta
        efetch -db protein -id ${PROTEIN_IDS[0]} -format fasta > ${ORIG_PROT_FILE}
        cat ${ORIG_PROT_FILE} | sed -E "s/>(.+)/>${ORGANISM_IDS[$i]}|${PROTEIN_IDS[0]}|${TEMPERATURES[$i]}/" > ${PROT_FILE}
        rm ${ORIG_PROT_FILE}
    fi
done 
