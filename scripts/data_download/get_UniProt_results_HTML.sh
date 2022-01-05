#!/bin/bash

set -ue

# A script to get UniProt search results in HTML from query with taxonomy ID

DATASET_FILE=$1

DOMAINS=($(tail -n +2 ${DATASET_FILE} | awk '{ print $2 }'))
TEMPERATURES=($(tail -n +2 ${DATASET_FILE} | awk '{ print $3 }'))
TAX_IDS=($(tail -n +2 ${DATASET_FILE} | awk '{ print $4 }'))

for((i = 0 ; i < "${#TAX_IDS[@]}" ; i++));
do
    echo "$i/${#TAX_IDS[@]}: fetching ${TAX_IDS[$i]}"
    PROTEOME_URL="https://www.uniprot.org/proteomes/?query=organism:"${TAX_IDS[$i]}"+redundant:no"
    RESULT_HTML="data/003/HTML/"${TAX_IDS[$i]}_${DOMAINS[$i]}_${TEMPERATURES[$i]}".html"
    curl -s ${PROTEOME_URL} > ${RESULT_HTML} 
done