#!/bin/bash

# A script that runs seqs_in_range.sh script for 
# several intervals of temperatures.

# Example usage:
# ./scripts/data_download/seqs_in_range_bulk.sh data/003/FASTA/ 0 6 [0-4] 1022

DIR=$1
FIRST=$2
SECOND=$3
STEP=$4
THRESHOLD=$5

for((i=${FIRST};i<=${SECOND};i++));
do
	if ! [ $i -eq 0 ]
	then
		echo "^$i${STEP}_.*";
		./scripts/data_download/seqs_in_range.sh ${DIR} "^$i${STEP}_.*" ${THRESHOLD};
	else
		echo "^${STEP}_.*";
		./scripts/data_download/seqs_in_range.sh ${DIR} "^${STEP}_.*" ${THRESHOLD};
	fi
done
