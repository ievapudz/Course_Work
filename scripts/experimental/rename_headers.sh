#!/bin/bash

# A script that renames a header of a FASTA record in the FASTA file
# with the name of the FASTA file.

# Example usage:
# ./scripts/experimental/rename_headers.sh data/experimental/10.1016_j.biortech.2019.01.049/FASTA/

FASTA_DIR=$1

FASTA_FILES=($(ls ${FASTA_DIR})) 

for((i = "0"; i < "${#FASTA_FILES}"; i++));
do
	NAME=$(basename "${FASTA_FILES[$i]}" .fasta)
	if [ -z "${FASTA_FILES[$i]}" ]
	then
		echo "Empty file, skipping"
	else
		echo "Renaming header in ${FASTA_FILES[$i]}"
		cat "${FASTA_DIR}/${FASTA_FILES[$i]}" | awk -v var=${NAME} '/^>/{print ">"var; next}{print}' > "${FASTA_DIR}/${FASTA_FILES[$i]}.tmp"
    	mv ${FASTA_DIR}/${FASTA_FILES[$i]}.tmp ${FASTA_DIR}/${FASTA_FILES[$i]} 	
	fi
done
