# Protein Classificator

## Prerequisites

- Python3 (tested on Python 3.7.4)
- [ESM](https://github.com/facebookresearch/esm) (v0.4.0)
- [PyMDE](https://github.com/cvxgrp/pymde) (v0.1.13)

## Primary dataset (001) for training

Firstly, proteomes of *Escherichia coli* (ECOLI, [UP000000625](https://www.uniprot.org/proteomes/UP000000625)) and *Sulfolobus solfataricus* (SACS2, [UP000001974](https://www.uniprot.org/proteomes/UP000001974)) were taken to train the model. Due to the growth conditions of each organism, *E. coli* was taken as a representative of mesophiles, assuming that the optimal conditions for its protein functionality is around 37 degrees Celsius (Jang et al. 2017). Meanwhile, *S. solfataricus* - a thermophile - has a proteome consisting of proteins, which have optimal conditions of 80 degrees Celsius (Zaparty et al. 2010).  The datasets consisted of 4392 and 2938 proteins for *E. coli* and *S. solfataricus* respectively. 

## Usage of protein embedding

Embedding is a technique to mapping from words to vectors, which allow to do a more convenient analysis in the model. Neural networks use embeddings to reduce the number of dimensions of categorical variables and meaningfully represent categories in the transformed space.

A couple of software tools to make embeddings were checked: `bio_embeddings` (Dallago et al. 2021) and a script to extract embeddings from Evolutionary Scale Modeling (ESM) (Rives et al. 2021).  The latter one was chosen to accomplish this task for our case of protein sequences. 

The following command was run to generate embeddings for the training dataset. The analogical commands were run for validation and testing datasets.

```
python3 extract.py esm1b_t33_650M_UR50S data/001/FASTA/training_sequences.fasta data/001/EMB_ESM1b/training_sequences/ --repr_layers 0 32 33 --include mean per_tok
```

Since embeddings took up a lot of storage space (~23 GB for training dataset and ~5 GB for each validation and testing sets), they were moved from the local storage to OneDrive.

## Removal of duplicated sequences

Initially generated sequences files were not taken as input to the embedding tool, since FASTA file that was run to try embedding included several sequences that had duplicates by the sequence. Therefore, the data parsing part was edited by removing encountered duplicates. There were 42 sequences removed from the initial dataset changing the overall number of sequences to 7288.

## Filtering sequences by length

The script to generate embeddings for our protein sequences did not process sequences that were longer than 1024 aminoacids. The visualisation package PyMDE required the embeddings to have the respective representation of each sequence in FASTA, therefore filtered FASTA files were generated.

1. The list of embeddings (PT format files named by the FASTA sequence ID) were listed down with command:

```
ls -1 > data/001/EMB_ESM1b/training_embeddings.lst
ls -1 > data/001/EMB_ESM1b/validation_embeddings.lst
ls -1 > data/001/EMB_ESM1b/testing_embeddings.lst
```

2. For the training dataset, due to the limitations of storage, only the sample of the set was taken. 

The size of the sample was set to be one quarter of the training dataset. 

The command that was run to get the number of all embeddings: 

```
ls -1 | wc -l
```

The output of the command was 5056 (at Mon Nov 15 15:26:47 CET 2021).

The command that was run to get the random sample of the training sequence list:

```
ls -1 | shuf -n 1264 > data/001/EMB_ESM1b/training_embeddings_sample.lst
```

The embedding files that were required for visualisation were picked with with command:

```
cat data/001/EMB_ESM1b/training_embeddings_sample.lst | xargs -I % cp % data/EMB_ESM1b/training_embeddings_sample/%
```

Those embeddings files were uploaded to Google Drive to access from Google Colab notebook.

3. Picking the FASTA sequences that had the generated embeddings and putting these sequences into the filtered FASTA files. The creation of filtered FASTA files was done in the `classificator.ipynb`.

## Visualisation of the dataset

The visualisation of the initial dataset was performed for a random sample of training dataset, and full sets of validation and testing. The visualisation was performed using two methods: PCA with `matplotlib.pyplot` package and PyMDE.

![training_sample_PCA_matplotlib](./data/001/visualisation/training_embeddings_sample_visualisation_matplotlib.png) 

**Fig. 1.** PCA plot made with matplotlib of the training dataset sample embeddings

![training_sample_PyMDE](./data/001/visualisation/training_embeddings_sample_visualisation_PyMDE.png) 

**Fig. 2.** Minimum-distortion embedding plot of the training dataset sample embeddings

The visualisation (Fig. 1. and Fig. 2.) of the dataset showed a significant distinction between the thermophilic and mesophilic prokaryote proteins. However, since the chosen prokaryotes were different not only in the living conditions, yet also they differed in their domains: *E. coli* belongs to bacteria domain, meanwhile *S. solfataricus* is an archaeon species. Therefore it was decided to make additional visualisations for mesophilic archaea and thermophilic bacteria proteomes.

## Analysis of the data clusters

Mesophilic archaea:
- *Methanobrevibacter oralis* (9EURY) [UP000077428](https://www.uniprot.org/proteomes/UP000077428)
- *Nitrosopumilus maritimus* (strain SCM1) (NITMS) [UP000000792](https://www.uniprot.org/proteomes/UP000000792)

Thermophilic bacteria:
- *Aquifex aeolicus* (strain VF5) (AQUAE) [UP000000798](https://www.uniprot.org/proteomes/UP000000798)
- *Thermotoga maritima* (strain ATCC 43589 / DSM 3109 / JCM 10099 / NBRC 100826 / MSB8) (THEMA) [UP000008183](https://www.uniprot.org/proteomes/UP000008183)

In order to check whether the clusterization in the primary dataset occurred due to the domain of the organism or the thermophilic properties of each protein, four cases of tests were performed: two to expect the positive result (clusterization effect into two groups resembling the initial plot) and other two with an expectation to observe the negative result - no distinctive classes.

Samples for positive tests:
- [x] 001. Sample containing mesophilic (UP000000625) and thermophilic bacteria (UP000000798, UP000008183).
- [x] 002. Sample containing mesophilic (UP000077428, UP000000792) and thermophilic (UP000001974) archaea.

Samples for negative tests:
- [x] 003. Sample containing thermophilic bacteria (UP000000798, UP000008183) and archaea (UP000001974).
- [x] 004. Sample containing mesophilic bacteria (UP000000625) and archaea (UP000077428, UP000000792).

In (py37) conda environment:
```
python3 esm/extract.py esm1b_t33_650M_UR50S data/cluster_tests/004/FASTA/004.fasta data/cluster_tests/004/EMB_ESM1b/ --repr_layers 0 32 33 --include mean per_tok
```

```
python3 scripts/positive_test.py
python3 scripts/negative_test.py
```

The output (plots) for these cluster tests were put to `data/cluster_tests/visualisation` directory.

## Usage of evolutionary scale modeling

Transformer protein language models from Facebook AI Research (Rives et al. 2019).

## Construction of the model

General logic of the workflow:

- Define the model in the separate module (loss function currently is defined separately - right before the beginning of the training).
- Load training and validation datasets (pregenerated embeddings).
- Define BATCH_SIZE and NUM_OF_EPOCHS (according to number of data elements).
- If needed, trim the dataset so that it would be the size of BATCH_SIZE multiple (function for that can be found in `scripts/model_dataset_processing.py`).
- Convert labels to binary (function for that can be found in `scripts/model_dataset_processing.py`).
- Pass processed datasets to `DataLoader`.
- Initialize the defined model.
- Set loss function and optimizer.
- Run epochs with training and validation functions (found in `scripts/model_flow.py`).

### Single-layer perceptron

The simplest model was composed of one linear layer that takes up all 1280 values from the embeddings vector. The activation function was chosen to be sigmoid, since it is compatible with binary cross entropy loss function. 

There were two alternatives applied: 
- Sigmoid activation and BCE loss functions were called separately
- BCEWithLogitsLoss function that wraps Softmax and BCE loss functions together. According to ... this alternative is more stable than the previous one.

The whole workflow will be in `scripts/classificator.py`.
Data processing functions are placed in `scripts/model_dataset_processing.py`.

### Dataset for SLP testing (002)

The first results (ROC curves) of SLP trained with two proteomes [*Escherichia coli* (ECOLI)](https://www.uniprot.org/proteomes/UP000000625) and [*Sulfolobus solfataricus* (SACS2)](https://www.uniprot.org/proteomes/UP000001974) were showed high accuracy of prediction, therefore it was decided to test the model with a different set of organisms that would contain more diverse species regarding the temperature that is optimal for the organism.

All files required for this dataset are placed in `data/002` directory. 

The sequences were taken from the [database](https://zenodo.org/record/1175609#.YcCVhS8Rq4o) (Engqvist, Martin Karl Magnus 2018) of growth temperatures of 21 498 organisms. It was decided to split the dataset to mesophiles and thermophiles and take 70%:15%:15% proportions for the datasets required to develop the model. Organisms that were divided into two groups: 
with temperature labels equal to 65 or above, and the group of organisms with temperature labels below (psychrophiles and mesophiles). 

The number of records in the dataset:
```
tail -n +2 data/002/TSV/temperature_data.tsv | wc -l
21498
```

Counting how many proteomes belong to thermophiles:
```
tail -n +2 data/002/TSV/temperature_data.tsv | awk '$3 >= 65 { print $3 }' | wc -l
283
```

Sorting, shuffling and saving the separate datasets:
```
tail -n +2 data/002/TSV/temperature_data.tsv | sort -k3 -n | head -n 21215 | gshuf > data/002/TSV/below_65_temperature_data.tsv
tail -n +2 data/002/TSV/temperature_data.tsv | sort -k3 -n | tail -n 283 | gshuf > data/002/TSV/above_65_temperature_data.tsv
```

Creating a training dataset:
```
cat data/002/TSV/below_65_temperature_data.tsv | head -n 14850 > data/002/TSV/training_temperature_data.tsv
cat data/002/TSV/above_65_temperature_data.tsv | head -n 198 >> data/002/TSV/training_temperature_data.tsv
```

Creating a validation dataset:
```
cat data/002/TSV/below_65_temperature_data.tsv | tail -n +14851 | head -n 3182 > data/002/TSV/validation_temperature_data.tsv
cat data/002/TSV/above_65_temperature_data.tsv | tail -n +199 | head -n 42 >> data/002/TSV/validation_temperature_data.tsv
```

Creating a testing dataset:
```
cat data/002/TSV/below_65_temperature_data.tsv | tail -n +18033 > data/002/TSV/testing_temperature_data.tsv
cat data/002/TSV/above_65_temperature_data.tsv | tail -n +241 >> data/002/TSV/testing_temperature_data.tsv
```

Each of the datasets require shuffling before usage in the model flow.

Since computational resources were limited, around 10 percent of proteomes could be downloaded. That was (expected):
- 1500 protein sequences from each organism in `data/002/TSV/training_temperature_data.tsv`
- 330 protein sequences from each organism in `data/002/TSV/validation_temperature_data.tsv`
- 330 protein sequences from each organism in `data/002/TSV/testing_temperature_data.tsv`

There was only 1 sequence taken from each organism (it was expected to get at least one sequence for an organism, since not all organisms had records in NCBI `protein` database). Since our model's predictions should not be biased by an organism,
thus it was assumed that this sample size should not be unsuitable for the task that is solved. 

Protein sequences were downloaded using the script `scripts/data_download/download_proteins_by_TaxID.sh` that uses `efetch 14.6`. The script requires improvement so that it would take `DATASET_FILE` and `INPUT_DIR` as command line arguments.

In order to use the flow described below, the initial dataset should be defined in the TSV file with required fields:
- $1 - name of organism species
- $2 - domain of an organism (not mandatory to be specified precisely)
- $3 - temperature label
- $4 - taxonomy ID of an organism

Alternatively, the dataset can be presented as a multiple FASTA file with headers in the format:
```
>organism_tax_id|protein_ID|temperature_label
```

If datasets are placed in separate training, validation and testing FASTA files, the flow can be started from the 4th point (embeddings generation). 

The steps for testing with 002 dataset:

1. Download training, validation, testing sets with:
```
./scripts/data_download/download_proteins_by_TaxID.sh data/002/TSV/training_temperature_data.tsv data/002/FASTA/training/ 1500
./scripts/data_download/download_proteins_by_TaxID.sh data/002/TSV/validation_temperature_data.tsv data/002/FASTA/validation/ 330
./scripts/data_download/download_proteins_by_TaxID.sh data/002/TSV/training_temperature_data.tsv data/002/FASTA/testing/ 330
```

2. All downloaded sequences for a dataset should be concatenated into one file: 
```
cat data/002/FASTA/training/*.fasta > data/002/FASTA/training/training.fasta
cat data/002/FASTA/validation/*.fasta > data/002/FASTA/validation/validation.fasta
cat data/002/FASTA/testing/*.fasta > data/002/FASTA/testing/testing.fasta
```

3. Generate embeddings:

Usage of the functions below does not give the intended flow, since the process stops after each set due to certain sequence lengths (the sequences of length above 1024 aminoacids are not processed by ESM):
```
generate_embeddings('esm/extract.py', data['train']['FASTA'], data['train']['embeddings'])
generate_embeddings('esm/extract.py', data['validate']['FASTA'], data['validate']['embeddings'])
generate_embeddings('esm/extract.py', data['test']['FASTA'], data['test']['embeddings'])
```

Recommended to generate embeddings using the following separate commands:
```
python3.7 esm/extract.py esm1b_t33_650M_UR50S data/002/FASTA/training/training.fasta data/002/EMB_ESM1b/training/ --repr_layers 0 32 33 --include mean per_tok

python3.7 esm/extract.py esm1b_t33_650M_UR50S data/002/FASTA/validation/validation.fasta data/002/EMB_ESM1b/validation/ --repr_layers 0 32 33 --include mean per_tok

python3.7 esm/extract.py esm1b_t33_650M_UR50S data/002/FASTA/testing/testing.fasta data/002/EMB_ESM1b/testing/ --repr_layers 0 32 33 --include mean per_tok
```

4. Save embeddings into NPZ files:
```
python3.7 scripts/002_embeddings.py
```

5. Run classificator model's training and validation with:
```
python3.7 scripts/002_classificator.py
```

Numbers of downloaded sequences:
- `data/002/FASTA/training/training.fasta`: 1263 headers were counted out of 1500 files attempted to download.
- `data/002/FASTA/validation/validation.fasta`: 281 headers were counted out of 330 files attempted to download.
- `data/002/FASTA/testing/testing.fasta`: 285 headers were counted out of 330 files attempted to download.

Generated embeddings:
- `data/002/ESM_EMB1b/training/`: 1214 out of 1263
- `data/002/ESM_EMB1b/validation/`: 268 out of 281
- `data/002/ESM_EMB1b/testing/`: 277 out of 285

### Dataset for SLP testing (003)

### Attempt #1 to fetch UniParc IDs

Using `curl` 18534 HTML UniProt search results in Proteomes database were downloaded. 

```
./scripts/data_download/get_UniProt_results_HTML.sh data/002/TSV/temperature_data.tsv
```

After the search results based on TaxIDs were downloaded to HTML files using `get_UniProt_results_HTML.sh`, they were 
parsed to extract UniParc IDs. The results were filtered using `ggrep` command to find UniParc 
identifiers for each organism:
```
ggrep -oP '/proteomes/UP.........' data/003/HTML/*.html > data/003/proteome_UniParc_IDs.txt
```

23098 identifiers were saved, thus it was needed to remove the redundant proteomes. Also, the temperature labels had to
be saved.

The list of UniParc identifiers and their respective taxonomy identifiers were saved into a TSV list:
```
cat data/003/proteome_UniParc_IDs.txt | tr ':' '\t' | sed 's/\/proteomes\///g' | sed 's/data\/003\/HTML\///g' | sed 's/\.html//g' > data/003/proteome_TaxIDs_UniParc_IDs.tsv
```

### Attempt #2 to fetch UniParc IDs

HTML files with proteome UniParc IDs were redownloaded with edited script `scripts/data_download/get_UniProt_results_HTML.sh` - HTML files were named in the format: `[TaxID]_[Domain]_[Temperature_label].html`. There were 19774 HTML files downloaded.

Extracting UniParc IDs for each organism's proteome:
```
ggrep -oP '/proteomes/UP.........' data/003/HTML/*.html > data/003/proteome_UniParc_IDs_non_redundant.txt
```

15223 UniParc IDs were saved. Observations from the generated list:
- not all organisms have got a proteome in UniProt database (result contained no UP identifier)
- not all organisms have got a reference proteome
- there are excluded proteomes shown in the results page (these proteomes should be filtered out)
- there are proteomes that belong different bacteria strains

### Attempt #3 to fetch UniParc IDs

This time the filter to reject excluded proteomes from the list was added.

The example URL:
```
https://www.uniprot.org/proteomes/?query=organism:50741+redundant:no+excluded:no
```

Extracting UniParc IDs for each organism's proteome:
```
ggrep -oP '/proteomes/UP.........' data/003/HTML/*.html > data/003/proteome_UniParc_IDs_non_redundant_no_excluded.txt
```

14537 UniParc IDs were saved.

The list of UniParc identifiers was saved to a TSV file:
```
cat data/003/proteome_UniParc_IDs_non_redundant_no_excluded.txt | tr ':' '\t' | sed 's/\/proteomes\///g' | sed 's/data\/003\/HTML\///g' | sed 's/\.html//g' > data/003/proteome_UniParc_IDs_non_redundant_no_excluded.tsv
```

There were 6411 unique `[TaxID]_[Domain]_[Temperature_label]` names in the list. The list contained several TaxIDs that referred to 
different species. For example, the taxonomy identifier 996 was assigned to *Flavobacterium columnare* (temperature 23 degrees Celsius),
*Flexibacter columnaris* (temperature 23 degrees Celsius), and *Cytophaga columnaris* (temperature 21 degrees Celsius).

It was decided to keep a single proteome for one taxonomy identifier. There were 5787 proteomes left in the final list:
```
awk -F"\t" '!_[$1]++' data/003/proteome_UniParc_IDs_non_redundant_no_excluded.tsv | awk -F"\t" '!_[$2]++' > data/003/003.tsv
```

Sorting based on temperature:
```
cat data/003/003.tsv | tr '_' '\t' | sort -n -k3 | awk '{print $3"_"$1"_"$2"\t"$4}' > data/003/003_sorted.tsv
cp data/003/003_sorted.tsv data/003/003.tsv
diff data/003/003_sorted.tsv data/003/003.tsv
rm data/003/003_sorted.tsv
```

### Downloading proteomes

An example query to download a non-redundant proteome:
```
curl "https://www.uniprot.org/uniprot/?query=proteome:UP000053199&format=fasta"
``` 

The proteome download script is `scripts/data_download/get_UniProt_proteomes.sh`.

Example usage:
```
./scripts/data_download/get_UniProt_proteomes.sh data/003/003.tsv
```

### Processing the dataset

#### v1 of 003 dataset 

Since the numbers of proteomes of each class are not equal - there were 5676 proteomes of the class 0 and 111 proteomes of the class 1 - it was decided to combine all proteins from the same class into one FASTA file, from which the proportions required for training, validation and testing would be divided. 

The number of proteins belonging to class 1 - 24723317.

The number of proteins belonging to class 1 - 212729.

Scripts that were used to generated training, validation and testing file sets:
```
./scripts/003_preembeddings.sh data/003/FASTA
./scripts/003_preembeddings.py data/003/FASTA
```

This approach divided all proteins into training, validation and testing sets without considering the TaxID of an organism 
that protein belongs to.

#### v2 of 003 dataset

This approach divides proteomes into training, validation and testing set. The sets are approximately balanced. 

Picking 111 proteomes from each class and shuffling the list of proteomes:
```
ls data/003/FASTA/  | tr '_' '\t' | head -n -6 | sort -n -k1 | awk '$1>=65{ print $1"_"$2"_"$3}' | shuf | \ 
tail -n 111 > data/003/class_1_111_proteomes.lst

ls data/003/FASTA/  | tr '_' '\t' | head -n -6 | sort -n -k1 | awk '$1<65{ print $1"_"$2"_"$3}' | shuf | \ 
tail -n 111 > data/003/class_0_111_proteomes.lst
```

The script `scripts/003_preembeddings_v2.sh` takes in a list of proteomes of a certain class, the intial index,
the number of files to take from the list, and the prefix of FASTA files (the directory, from which the proteomes will be taken).
```
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 0 77 data/003/FASTA/  > data/003/FASTA/training_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 77 17 data/003/FASTA/ > data/003/FASTA/validation_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_1_111_proteomes.lst 94 17 data/003/FASTA/ > data/003/FASTA/testing_v2.fasta 

./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 0 32 data/003/FASTA/ >> data/003/FASTA/training_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 32 8 data/003/FASTA/ >> data/003/FASTA/validation_v2.fasta 
./scripts/003_preembeddings_v2.sh data/003/class_0_111_proteomes.lst 40 11 data/003/FASTA/ >> data/003/FASTA/testing_v2.fasta 
```

| Set         | # of proteomes (overall, class_0, class_1) | # of proteins (overall, class_0, class_1) | 
|-------------|--------------------------------------------|-------------------------------------------|
| training    | 109, 32, 77                                | 288996, 145128, 143868                    |
| validation  | 25, 8, 17                                  | 65820, 33204, 32616                       |
| testing     | 28, 11, 17                                 | 74508, 38263, 36245                       |


FASTA-splitter program was used to divide each of the sets into portions:
```
../programs/fasta-splitter.pl --n-parts 30 --out-dir data/003/FASTA/training_v2/ \ 
    --nopad data/003/FASTA/training_v2/training_v2.fasta
../programs/fasta-splitter.pl --n-parts 7 --out-dir data/003/FASTA/validation_v2/ \
    --nopad data/003/FASTA/validation_v2/validation_v2.fasta
../programs/fasta-splitter.pl --n-parts 8 --out-dir data/003/FASTA/testing_v2/ \ 
    --nopad data/003/FASTA/testing_v2/testing_v2.fasta
```

### Generating embeddings (testing slurm)

It is required to make sure that directories for embeddings are created.

In order to test the slurm submission script (for the first 1000 FASTA sequences in validation set), 
the sample FASTA file was created using:
```
cat data/003/FASTA/validation.fasta | perl -e '{ $num = 1000; $/ = "\n>"; }{ while(<>){ if($num==0){ exit; } /^>?([^\n]*)\n([^>]*)/; my( $header, $sequence ) = ( $1, $2 ); print ">", $1, "\n", $2, "\n"; $num--; } }' > data/003/FASTA/validation_0_999.fasta
```

Embeddings for a set in `data/003/FASTA/validation_0_999.fasta` were generated on a computing cluster. It was the first sample
for testing `slurm` compatability with `conda` virtual environment.

A command that was used to run the program on a cluster:
```
sbatch scripts/003_embeddings.sh
```

For the first set 975/1000 sequence embeddings were generated.

### Generating embeddings (003 v2)

```
sbatch --array=1-30 --output=training_v2.part-%a.slurm-%A_%a.out scripts/003/003_embeddings_training_v2.sh

sbatch --array=1-7 --output=validation_v2.part-%a.slurm-%A_%a.out scripts/003/003_embeddings_validation_v2.sh

sbatch --array=1-8 --output=testing_v2.part-%a.slurm-%A_%a.out scripts/003/003_embeddings_testing_v2.sh
```

| Set         | # of embeddings (of all proteins) | # of embeddings (class_0) | # of embeddings (class_1) |
|-------------|-----------------------------------|---------------------------|---------------------------|
| training    |  284309 (288996)                  | 141602 (145128)           | 142707 (143868)           |
| validation  |  65156 (65820)                    | 32793 (33204)             | 32363 (32616)             |
| testing     |  73663 (74508)                    | 37749 (38263)             | 35913 (36245)             |

## Correlation between training set true temperature labels and 003 predictions

After running the testing phase:
```
./scripts/003/003_classificator_testing.py
```

Two temporary files will be generated: `data/003/temperature_predictions_correlation_x.lst` and `data/003/temperature_predictions_correlation_y.lst`. These files will be used in `./scripts/003/003_correlation.sh` script, which
can be run the following way:

`conda` environment with `pandas` package installed is required for the script
```
conda activate py37_pandas
./scripts/003/003_correlation.sh results/SLP/003/temperature_predictions_correlation.png 
```

### Dataset for SLP testing (004)

This dataset will contain only representatives of clusters. The clusters will be generated using `cd-hit` program 
(version 4.8.1).

The FASTA file with all embedded sequences (423127) from 003 dataset (`data/004/FASTA/004.fasta`) was composed:
```
./scripts/004/004_filtered_FASTA.py > data/004/FASTA/004.fasta
```

The clusters were made using `cd-hit` program. 
Option meanings :
- -d - length of description in CLSTR file
- -c - sequence identity threshold
- -T - number of threads used
- -M - maximum available memory (Mbyte)
- -i - the name of an input file
- -o - the name of an output file

```
conda activate cd-hit

cd-hit -d 0 -c 0.9 -T 0 -M 15000 -i data/004/FASTA/004.fasta -o data/004/FASTA/004_c_90.fasta
cd-hit -d 0 -c 1 -T 0 -M 15000 -i data/004/FASTA/004.fasta -o data/004/FASTA/004_c_100.fasta
```

| File                            | # of clusters | # of class_0 proteomes | # of class_1 proteomes |
|---------------------------------|---------------|------------------------|------------------------|
| data/004/FASTA/004_c_90.fasta   |      391795   |                     51 |                    111 |
| data/004/FASTA/004_c_100.fasta  |      418958   |                    TBU |                    TBU |


## Tasks to do

- [x] Extract UniProt accession numbers from initial FASTA files.
- [x] Create FASTA files `*_sequences.fasta` which records contain only UniProt accession numbers in the header.
- [x] Create `*_temperature_annotations.csv` files that contain identifier and temperature labels.
- [x] Set up `config.yml` file to use the embedding.
- [x] Try evolutionary scale modeling (generation of embeddings).
- [x] Visualise generated embeddings for a random sample of training dataset.
- [x] Visualise generated embeddings for validation dataset.
- [x] Visualise generated embeddings for testing dataset.
- [x] Remove variant effect scale from the PCA visualisation.
- [x] Separate modules in `classificator.ipynb` for an easier usage of its functionalities in the future.
- [x] Construct a simple neural network (a single layer perceptron).
- [x] Create mesophilic archaea and thermophilic bacteria embeddings.
- [x] Visualise mesophilic archaea and thermophilic bacteria embeddings.
- [ ] Determine the species that are taken into PyMDE for visualisation automatically.
- [x] Determine the order of species that are taken into PyMDE for visualisation (answer: alphabetical order).
- [x] Construct a simple neural network (a single layer perceptron) with tools from PyTorch package.
- [ ] Construct another simple neural network (with a single hidden layer 1DCNN, RELU) with a softmax activation function as an output. 
- [x] Automate model training process and separate modules to make the process adaptive to different architectures.
- [ ] Include loss functions in the definition of the model.
- [x] Include ROC curve graphing.
- [x] Include printing of confusion matrices.
- [x] Generate a new training and validation sets from the [microorganism dataset](https://zenodo.org/record/1175609#.YbtlfC8RpQJ) with growth temperature annotations.
- [x] Train and validate SLP with a new generated training and validation set.
- [x] Improve script in `scripts/data_download` to take input dataset file and input directory as command line arguments.
- [x] Visualise 002 dataset embeddings.
- [x] Download HTML format results with reference genome UniParc identifiers.
- [x] Grep UniParc identifiers from HTML results with `ggrep "/proteomes/UP........."`
- [x] Save only TaxID and UniParc ID in the list of 003 proteome IDs.
- [x] Download non-redundant proteome UP IDs (run modified (appended `redundant:no`) `get_UniProt_results_HTML.sh`).
- [x] Save temperature labels in the list with Tax IDs and UniParc IDs.
- [ ] Count how many proteins are found in NCBI database (from organisms in the given `temperature_data.tsv` database).
- [x] Download proteomes to HPC.
- [x] Make rainbow-coloured ROC curves.
- [x] Generate 003 embeddings (mean) for 10-30 proportions of the training set (remaining, currently running 10-16).
- [x] Generate 003 embeddings (mean) for 3-7 proportions of the validation set (remaining, currently running 3-4).
- [x] Generate 003 embeddings (mean) for 1-8 proportions of the testing set.

## References

1. Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. 2021. "Learned embeddings from deep learning to visualize and predict protein sets." *Current Protocols*, 1, e113. https://doi.org/10.1002/cpz1.113. 

2. Jang, J., Hur, H. G., Sadowsky, M. J., Byappanahalli, M. N., Yan, T., & Ishii, S. 2017. "Environmental Escherichia coli: ecology and public health implications—a review." *Journal of applied microbiology*, 123(3), 570-581. https://doi.org/10.1111/jam.13468.

3. Rives, A., Meier, J., Sercu, T., Goyal, S., Lin, Z., Liu, J., ... & Fergus, R. 2021. "Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences." *Proceedings of the National Academy of Sciences*, 118(15). https://doi.org/10.1073/pnas.2016239118.

4. Zaparty, M., Esser, D., Gertig, S., Haferkamp, P., Kouril, T., Manica, A., ... & Siebers, B. 2010. "'Hot standards' for the thermoacidophilic archaeon Sulfolobus solfataricus." Extremophiles, 14(1), 119-142. https://doi.org/10.1007/s00792-009-0280-0.

5. Engqvist, Martin Karl Magnus. 2018. "Growth temperatures for 21,498 microorganisms (1.0.0)" [Data set]. Zenodo. https://doi.org/10.5281/zenodo.1175609

6. Engqvist, M. K. 2018. "Correlating enzyme annotations with a large set of microbial growth temperatures reveals metabolic adaptations to growth at diverse temperatures." *BMC microbiology*, 18(1), 1-14. https://doi.org/10.1186/s12866-018-1320-7.

7. Fu, L., Niu, B., Zhu, Z., Wu, S., & Li, W. (2012). CD-HIT: accelerated for clustering the next-generation sequencing data. Bioinformatics, 28(23), 3150-3152. https://academic.oup.com/bioinformatics/article/28/23/3150/192160?login=true

