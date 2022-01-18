#!/bin/bash

# This is a script that divides the general list of dataset into class 0 and class 1.

# The partition is made based on temeprature labels: the proteomes of temperature less
# than 65 are assigned to the class 0, and the remaining proteomes are assigned to 
# the class 1.

set -ue

FASTA_FILE_DIR=$1
CLASS_0_FASTA=${FASTA_FILE_DIR}/class_0.fasta
CLASS_1_FASTA=${FASTA_FILE_DIR}/class_1.fasta

FASTA_FILES=($(ls $FASTA_FILE_DIR | tr '_' '\t' | sort -n -k1 | awk -v FASTA_FILE_DIR=${FASTA_FILE_DIR} '{print FASTA_FILE_DIR"/"$1"_"$2"_"$3}'))
TEMPERATURE_LABELS=($(ls $FASTA_FILE_DIR | tr '_' '\t' | sort -n -k1 | awk '{print $1}'))
TAX_IDS=($(ls $FASTA_FILE_DIR | tr '_' '\t' | sort -n -k1 | awk '{print $2}'))

for((i = 0 ; i < "${#FASTA_FILES[@]}" ; i++));
do 
    TAX_ID=${TAX_IDS[$i]}
    export TAX_ID
    TEMPERATURE_LABEL=${TEMPERATURE_LABELS[$i]}
    export TEMPERATURE_LABEL
    if [ "${TEMPERATURE_LABEL}" -ge 65 ]
    then  
    	cat ${FASTA_FILES[$i]} | tr '|' '_' | perl ./scripts/003_preembeddings.pl >> ${CLASS_1_FASTA}
    else
        cat ${FASTA_FILES[$i]} | tr '|' '_' | perl ./scripts/003_preembeddings.pl >> ${CLASS_0_FASTA}
    fi
done
