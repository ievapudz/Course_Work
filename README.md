# Repository for Protein Thermostability Prediction

This repository contains files that were used to execute protein 
thermostability prediction using sequence representations from
a protein language model research. 

## Data download

Using `curl` 18534 HTML UniProt search results in Proteomes 
database were downloaded. Downloaded HTML files were parsed
to extract UniParc IDs.

```
./scripts/data_download/get_UniProt_results_HTML.sh \
	data/002/TSV/temperature_data.tsv
```

The results were filtered using `ggrep` command to find
UniParc identifiers for each organism:

```
ggrep -oP '/proteomes/UP.........' data/003/HTML/*.html > \
	data/003/proteome_UniParc_IDs_non_redundant_no_excluded.txt
```

14537 UniParc IDs were saved.

```
cat data/003/proteome_UniParc_IDs_non_redundant_no_excluded.txt | \
tr ':' '\t' | sed 's/\/proteomes\///g' | sed 's/data\/003\/HTML\///g' | \
sed 's/\.html//g' > \
data/003/proteome_TaxIDs_UniParc_IDs_non_redundant_no_excluded.tsv
```

There were 6411 unique `[TaxID]_[Domain]_[Temperature_label]` names in the 
list. The list contained several TaxIDs that referred to 
different species. For example, the taxonomy identifier 996 was assigned 
to *Flavobacterium columnare* (temperature 23 degrees Celsius),
*Flexibacter columnaris* (temperature 23 degrees Celsius), and 
*Cytophaga columnaris* (temperature 21 degrees Celsius).

It was decided to keep a single proteome for one taxonomy identifier. 
There were 5787 proteomes left in the final list:
```
awk -F"\t" '!_[$1]++' \
data/003/proteome_UniParc_IDs_non_redundant_no_excluded.tsv | \
awk -F"\t" '!_[$2]++' > data/003/003.tsv
```

Sorting based on temperature:
```
cat data/003/003.tsv | tr '_' '\t' | sort -n -k3 | \
awk '{print $3"_"$1"_"$2"\t"$4}' > data/003/003_sorted.tsv
cp data/003/003_sorted.tsv data/003/003.tsv
diff data/003/003_sorted.tsv data/003/003.tsv
rm data/003/003_sorted.tsv
```

An example query to download a non-redundant proteome:
```
curl "https://www.uniprot.org/uniprot/?query=proteome:UP000053199&format=fasta"
``` 

The proteome download script is `scripts/data_download/get_UniProt_proteomes.sh`.

Example usage:
```
./scripts/data_download/get_UniProt_proteomes.sh data/003/003.tsv
```

## Data processing

The data set was divided into training, validation, and testing subsets, which
were approximatelly balanced and had non-overlapping taxonomy identifiers
between the sets.

Picking 111 proteomes from each class and shuffling the list of proteomes:
```
ls data/003/FASTA/  | tr '_' '\t' | head -n -6 | sort -n -k1 | \
awk '$1>=65{ print $1"_"$2"_"$3}' | shuf | \ 
tail -n 111 > data/003/class_1_111_proteomes.txt

ls data/003/FASTA/  | tr '_' '\t' | head -n -6 | sort -n -k1 | \
awk '$1<65{ print $1"_"$2"_"$3}' | shuf | \ 
tail -n 111 > data/003/class_0_111_proteomes.txt
```

The script `scripts/003_preembeddings_v2.sh` takes the following arguments:
- a list of proteomes of a certain class
- the initial index
- the number of files to take from the list
- the prefix of FASTA files (the directory of the proteomes)

```
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 0 77 \
data/003/FASTA/ > data/003/FASTA/training_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 77 17 \
data/003/FASTA/ > data/003/FASTA/validation_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 94 17 \
data/003/FASTA/ > data/003/FASTA/testing_v2.fasta 

./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 0 32 \
data/003/FASTA/ >> data/003/FASTA/training_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 32 8 \
data/003/FASTA/ >> data/003/FASTA/validation_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 40 11 \
data/003/FASTA/ >> data/003/FASTA/testing_v2.fasta 
```

| Set		  | # of proteomes (overall, class_0, class_1) | # of proteins (overall, class_0, class_1) | 
|-------------|--------------------------------------------|-------------------------------------------|
| training	  | 109, 32, 77								   | 288996, 145128, 143868				  	   |
| validation  | 25, 8, 17								   | 65820, 33204, 32616					   |
| testing	  | 28, 11, 17								   | 74508, 38263, 36245					   |


[FASTA-splitter](http://kirill-kryukov.com/study/tools/fasta-splitter/) 
program was used to divide each of the sets into portions:
```
../programs/fasta-splitter.pl --n-parts 30 --out-dir data/003/FASTA/training_v2/ \ 
    --nopad data/003/FASTA/training_v2/training_v2.fasta
../programs/fasta-splitter.pl --n-parts 7 --out-dir data/003/FASTA/validation_v2/ \
    --nopad data/003/FASTA/validation_v2/validation_v2.fasta
../programs/fasta-splitter.pl --n-parts 8 --out-dir data/003/FASTA/testing_v2/ \ 
    --nopad data/003/FASTA/testing_v2/testing_v2.fasta
```

## Generating embeddings 

```
sbatch --array=1-30 --output=training_v2.part-%a.slurm-%A_%a.out \
	scripts/003/003_embeddings_training_v2.sh
sbatch --array=1-7 --output=validation_v2.part-%a.slurm-%A_%a.out \
	scripts/003/003_embeddings_validation_v2.sh
sbatch --array=1-8 --output=testing_v2.part-%a.slurm-%A_%a.out \
	scripts/003/003_embeddings_testing_v2.sh
```

| Set         | # of all proteins embeddings      | # of class_0 embeddings   | # of class_1 embeddings   |
|-------------|-----------------------------------|---------------------------|---------------------------|
| training    |  284309 (288996)                  | 141602 (145128)           | 142707 (143868)           |
| validation  |  65156 (65820)                    | 32793 (33204)             | 32363 (32616)             |
| testing     |  73663 (74508)                    | 37749 (38263)             | 35913 (36245)             |


## Visualisation of embeddings

```
./scripts/003/003_visualisation.py
```

## Saving embeddings to CSV files

In order to make embeddings data more universal for processing with 
various software tools, it was decided to save embeddings in CSV files. 
The files are headerless. The values are listed in order of:
- #0 Taxonomy ID of the organism, to which the sequence belongs
- #1 Accession ID of the sequence
- #2 Length of the sequence
- #3 Temperature label
- #4 - #1283 Components of embeddings 

```
./scripts/003/003_convert_NPZ_to_CSV_training.py > data/003/CSV/training_v2.csv
./scripts/003/003_convert_NPZ_to_CSV_validation.py > data/003/CSV/validation_v2.csv
./scripts/003/003_convert_NPZ_to_CSV_testing.py > data/003/CSV/testing_v2.csv
```

| File (in `data/003/CSV`) | Size (GB)   |
|--------------------------|-------------|
| training_v2.csv          | 3.034       |
| validation_v2.csv        | 0.696       |
| testing_v2.csv           | 0.786       |

## Training, validating, and testing the model

```
./scripts/003/003_classificator_inferences_testing.py
```

## Matthew's correlation coefficient (MCC) for 003 v2 testing

A function `calculate_MCC()` in `scripts/file_actions.py` was 
implemented to calculate MCC. The function 
takes in a TSV file in which there are two columns: a column of 
true temperature labels (normalised by division of 100)
and a column of predictions (values from 0 to 1). The function 
was called in script `scripts/003/003_calculate_MCC.py`.

```
./scripts/003/003_calculate_MCC.py -p \
	results/SLP/003/validation_predictions_epoch_5.tsv --true-label-idx 0 \
	--prediction-idx 1 --threshold 0.65 --header

./scripts/003/003_calculate_MCC.py -p \
	results/SLP/003/testing_v2_predictions.tsv --true-label-idx 2 \
	--prediction-idx 3 --threshold 65
```

MCC for 003 v2 validation (final epoch) was: 0.84278. 
MCC for 003 v2 testing was: 0.8478.

## Plotting distribution histogram 003

Commands to plot protein sequence distribution histogram for the subsets:
```
./scripts/003/003_plot_histogram.py data/003/TSV/training_v2_tensors.tsv 3 \
	data/003/visualisation_v2/training_v2_histo.png Training
./scripts/003/003_plot_histogram.py data/003/TSV/validation_v2_tensors.tsv 3 \
	data/003/visualisation_v2/validation_v2_histo.png Validation
./scripts/003/003_plot_histogram.py data/003/TSV/testing_v2_tensors.tsv 3 \
	data/003/visualisation_v2/testing_v2_histo.png Testing
```

