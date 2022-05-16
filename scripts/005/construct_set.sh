#!/bin/sh

# A script that constructs data set 005

LINE=$1

FASTA_FILES=($(shuf --random-source=data/005/TSV/005.tsv data/005/TSV/005_2.tsv | ${LINE}|\
			awk '{ if( $1 < 40 ) print "data/003/FASTA/" $1 "_" $2 "_" $3 }'))

for((i = 0 ; i < "${#FASTA_FILES[@]}" ; i++));
do 
	echo "${FASTA_FILES[$i]}"
	TEMPERATURE=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $1}')
	TAXID=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $2}')	
	cat ${FASTA_FILES[$i]} | sed "s/^>tr|\(.*\)|.*$/>$TAXID|\1|$TEMPERATURE/g"
done

FASTA_FILES=($(shuf --random-source=data/005/TSV/005.tsv data/005/TSV/005_2.tsv | ${LINE}|\
            awk '{ if( $1 >= 40 && $1 < 65 ) print "data/003/FASTA/" $1 "_" $2 "_" $3 }'))

for((i = 0 ; i < "${#FASTA_FILES[@]}" ; i++));
do
    echo "${FASTA_FILES[$i]}"
    TEMPERATURE=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $1}')
    TAXID=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $2}')
    cat ${FASTA_FILES[$i]} | sed "s/^>tr|\(.*\)|.*$/>$TAXID|\1|$TEMPERATURE/g"
done

FASTA_FILES=($(shuf --random-source=data/005/TSV/005.tsv data/005/TSV/005_2.tsv | ${LINE}|\
            awk '{ if( $1 >= 65 ) print "data/003/FASTA/" $1 "_" $2 "_" $3 }'))

for((i = 0 ; i < "${#FASTA_FILES[@]}" ; i++));
do
    echo "${FASTA_FILES[$i]}"
    TEMPERATURE=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $1}')
    TAXID=$(basename ${FASTA_FILES[$i]} | tr '_' '\t' | awk '{print $2}')
    cat ${FASTA_FILES[$i]} | sed "s/^>tr|\(.*\)|.*$/>$TAXID|\1|$TEMPERATURE/g"
done
