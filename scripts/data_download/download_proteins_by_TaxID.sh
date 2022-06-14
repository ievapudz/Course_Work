#!/bin/bash

set -ue

# A script to download protein sequences based on taxonomy IDs of organisms

DATASET_FILE=$1
OUT_DIR=$2
SAMPLE_SIZE=$3
HALF_SAMPLE=$(expr $SAMPLE_SIZE / 2)

ORGANISM_IDS=($(cat ${DATASET_FILE} | awk '{ print $4 }' | head -n ${HALF_SAMPLE}))
ORGANISM_IDS+=($(cat ${DATASET_FILE} | awk '{ print $4 }' | tail -n ${HALF_SAMPLE}))
TEMPERATURES=($(cat ${DATASET_FILE} | awk '{ print $3 }'| head -n ${HALF_SAMPLE}))
TEMPERATURES+=($(cat ${DATASET_FILE} | awk '{ print $3 }'| tail -n ${HALF_SAMPLE}))

DB='protein'
BASE='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

for((i = 0 ; i < "${SAMPLE_SIZE}" ; i++));
do
	ESEARCH_PROTEIN_URL=$BASE"esearch.fcgi?db=protein&term=txid${ORGANISM_IDS[$i]}[Organism:noexp]&usehistory=y"
	PROTEIN_IDS=($(curl -s ${ESEARCH_PROTEIN_URL} | grep '<Id>' | sed -n 's:.*<Id>\(.*\)</Id>.*:\1:p'))
	if [ "${#PROTEIN_IDS[@]}" != 0 ]
	then
		echo "$i/${#ORGANISM_IDS[@]} Downloading: ${PROTEIN_IDS[0]} ${#PROTEIN_IDS[@]}"
		for((j = 0 ; j < "${#PROTEIN_IDS[@]}" ; j++));
		do
			echo "${PROTEIN_IDS[$j]}"
		done
	fi
done 
