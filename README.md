# Protein Classificator

## Prerequisites

- Python3 (tested on Python 3.7.4)

## Primary dataset for training

Firstly, proteomes of *Escherichia coli* (https://www.uniprot.org/proteomes/UP000000625) and *Sulfolobus solfataricus* (https://www.uniprot.org/proteomes/UP000001974) were taken to train the model. Due to the growth conditions of each organism, *E. coli* was taken as a representative of mesophiles, assuming that the optimal conditions for its protein functionality is around 37 degrees Celsius (Jang et al. 2017). Meanwhile, *S. solfataricus* - a thermophile - has a proteome consisting of proteins, which have optimal conditions of 80 degrees Celsius (Zaparty et al. 2010).  The datasets consisted of 4392 and 2938 proteins for *E. coli* and *S. solfataricus* respectively. 

## Usage of protein embedding

Embedding is a technique to mapping from words to vectors, which allow to do a more convenient analysis in the model. Neural networks use embeddings to reduce the number of dimensions of categorical variables and meaningfully represent categories in the transformed space.

The protein embedding software `bio_embeddings` (Dallago et al. 2021) was chosen to accomplish this task for our case of protein sequences. The initial dataset of proteomes of two bacteria was prepocessed according to Basic Protocol 1: `config.yml` and `temperature_annotations.csv` files were created.

## Removal of duplicated sequences

Initially generated sequences files were not taken as input to the embedding tool, since FASTA file that was run to try embedding included several sequences that had duplicates by the sequence. Therefore, the data parsing part was edited by removing encountered duplicates. There were 42 sequences removed from the initial dataset changing the overall number of sequences to 7288.

### Tasks to do

- [x] Extract UniProt accession numbers from initial FASTA files.
- [x] Create FASTA files `*_sequences.fasta` which records contain only UniProt accession numbers in the header.
- [x] Create `*_temperature_annotations.csv` files that contain identifier and temperature labels.
- [x] Set up `config.yml` file to use the embedding.
- [x] Try evolutionary scale modeling (generation of embeddings).
- [ ] Visualise generated embeddings for a random sample of training dataset.
- [x] Visualise generated embeddings for validation dataset.
- [x] Visualise generated embeddings for testing dataset.

## Visualisation of the dataset

The visualisation of the initial dataset was performed for a random sample of training dataset, and full sets of validation and testing. The visualisation was performed using two methods: PCA with matplotlib.pyplot package and PyMDE.

## Usage of evolutionary scale modeling

Transformer protein language models from Facebook AI Research (Rives et al., 2019).

## References

1. Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, 1, e113. doi: 10.1002/cpz1.113. https://currentprotocols.onlinelibrary.wiley.com/doi/10.1002/cpz1.113

2. Jang, J., Hur, H. G., Sadowsky, M. J., Byappanahalli, M. N., Yan, T., & Ishii, S. (2017). Environmental Escherichia coli: ecology and public health implications—a review. Journal of applied microbiology, 123(3), 570-581. https://sfamjournals.onlinelibrary.wiley.com/doi/full/10.1111/jam.13468

3. Rives, A., Meier, J., Sercu, T., Goyal, S., Lin, Z., Liu, J., ... & Fergus, R. (2021). Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. Proceedings of the National Academy of Sciences, 118(15).

4. Zaparty, M., Esser, D., Gertig, S., Haferkamp, P., Kouril, T., Manica, A., ... & Siebers, B. (2010). “Hot standards” for the thermoacidophilic archaeon Sulfolobus solfataricus. Extremophiles, 14(1), 119-142. https://link.springer.com/article/10.1007/s00792-009-0280-0

