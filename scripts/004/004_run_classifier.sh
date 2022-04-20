#bin/sh

# Script that runs a batch of 004 classifier variations (different hyperparameters)

LEARNING_RATES=(1e-3 1e-4 1e-5)
BATCHES=(24 48 96)
EPOCHS=(5 50 100)

for((i = "0"; i < "${#LEARNING_RATES[@]}"; i++));
do
	for((j = "0"; j < "${#BATCHES[@]}"; j++));
	do
		for((k = "0"; k < "${#EPOCHS[@]}"; k++));
		do
			PRED_TXT="results/MultiClass1/004/l${LEARNING_RATES[$i]}_b${BATCHES[$j]}_e${EPOCHS[$k]}.txt"
			MODEL_PT="results/MultiClass1/004/l${LEARNING_RATES[$i]}_b${BATCHES[$j]}_e${EPOCHS[$k]}.pt"
			echo "Training ${MODEL_PT}"			
			srun --ntasks 1 ./scripts/004/004_classifier.py -n data/004/NPZ/training_and_validation_embeddings.npz \
				-l ${LEARNING_RATES[$i]} -b ${BATCHES[$j]} -r results/MultiClass1/004/ROC/ \
				-e "${EPOCHS[$k]}" -m "${MODEL_PT}" > ${PRED_TXT}  
		done
	done
done 
