#!/bin/bash

set -ue

LIST_OF_FILES=$1
INITIAL_INDEX=$2
NUMBER_OF_FILES=$3
PREFIX=$4

FILES=($(cat ${LIST_OF_FILES}))

#FASTA_FILES=($(ls $FASTA_FILE_DIR | tr '_' '\t' | sort -n -k1 | awk -v FASTA_FILE_DIR=${FASTA_FILE_DIR} '{print FASTA_FILE_DIR"/"$1"_"$2"_"$3}'))
TEMPERATURE_LABELS=($(cat ${LIST_OF_FILES} | tr '_' '\t' | awk '{print $1}'))
TAX_IDS=($(cat ${LIST_OF_FILES} | tr '_' '\t' | awk '{print $2}'))

END_INDEX=$(($INITIAL_INDEX+$NUMBER_OF_FILES))

for((i = "${INITIAL_INDEX}"; i < "${END_INDEX}" ; i++));
do
    TAX_ID=${TAX_IDS[$i]}
    export TAX_ID
    TEMPERATURE_LABEL=${TEMPERATURE_LABELS[$i]}
    export TEMPERATURE_LABEL
    cat ${PREFIX}${FILES[$i]} | tr '|' '_' | perl ./scripts/003_preembeddings.pl
done


