#!/bin/sh

# Script that runs a batch of 004 model  variations (different hyperparameters)

# Example usage:
# ./scripts/004/004_run_model.sh scripts/004/004_classifier_2.py results/MultiClass2/004
# ./scripts/004/004_run_model.sh scripts/004/004_regressor.py results/regressor/004

CLASSIFIER=$1
RES_DIR=$2

if [ ! -d "${RES_DIR}" ];
then
	mkdir "${RES_DIR}"
fi

LEARNING_RATES=(1e-3 1e-4 1e-5)
BATCHES=(24 48 96)
EPOCHS=(5 50 100)

for((i = "0"; i < "${#LEARNING_RATES[@]}"; i++));
do
	for((j = "0"; j < "${#BATCHES[@]}"; j++));
	do
		for((k = "0"; k < "${#EPOCHS[@]}"; k++));
		do
			PRED="${RES_DIR}/l${LEARNING_RATES[$i]}_b${BATCHES[$j]}_e${EPOCHS[$k]}.tsv"
			MODEL_PT="${RES_DIR}/l${LEARNING_RATES[$i]}_b${BATCHES[$j]}_e${EPOCHS[$k]}.pt"
			echo "Training ${MODEL_PT}"			
			srun --ntasks 1 ./${CLASSIFIER} -n data/004/NPZ/training_and_validation_embeddings.npz \
				-l ${LEARNING_RATES[$i]} -b ${BATCHES[$j]} -r ${RES_DIR}/ROC/ \
				-e "${EPOCHS[$k]}" -m "${MODEL_PT}" > ${PRED}  
		done
	done
done 
