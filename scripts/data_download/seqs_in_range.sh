#!/bin/sh

# A script that counts how many sequences there are in
# proteome FASTA files that are shorter than $3

# Usage:
# ./scripts/data_download/seqs_in_range.sh data/003/FASTA/ ^9[5-9]_* 1022 

DIR=$1
REGEX=$2
LENGTH=$3

FASTAS=($(ls ${DIR} | egrep "${REGEX}"))

SUM=0

for i in "${FASTAS[@]}"
do
	LINES=($(awk -v RS='>[^\n]+\n' -v LEN="$LENGTH" 'length() < LEN {printf "%s", prt $0} {prt = RT}' $DIR/$i | grep '>' | wc -l))
	SUM=$(($SUM+$LINES))
done

echo "$SUM"
