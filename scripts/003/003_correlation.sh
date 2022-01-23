#!/bin/sh

# A script that creates a PNG file of plot correlation
# between true temperature labels and the predicted 
# values.

# Example run:
# ./scripts/003/003_correlation.sh results/SLP/003/temperature_predictions_correlation.png 

X_VALUES_LIST=data/003/temperature_predictions_correlation_x.lst
Y_VALUES_LIST=data/003/temperature_predictions_correlation_y.lst
OUT_PNG_FILE=$1
OUT_TSV_FILE=./data/003/$(basename ${OUT_PNG_FILE} .png).tsv

touch ${OUT_TSV_FILE}
echo -e "temperature\tprediction" > ${OUT_TSV_FILE}
paste ${X_VALUES_LIST} ${Y_VALUES_LIST} | awk '{print $1/100"\t"$2}' >> ${OUT_TSV_FILE}

rm ${X_VALUES_LIST} ${Y_VALUES_LIST}

python3.7 ./scripts/003/003_plot_correlation.py ${OUT_TSV_FILE} ${OUT_PNG_FILE} 
