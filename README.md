# Protein Classificator

## Prerequisites

- Python3 (tested on Python 3.7.4)

## Primary dataset for training

Firstly, proteomes of *Escherichia coli* (https://www.uniprot.org/proteomes/UP000000625) and *Sulfolobus solfataricus* (https://www.uniprot.org/proteomes/UP000001974) were taken to train the model. Due to the growth conditions of each organism, *E. coli* was taken as a representative of mesophiles, assuming that the optimal conditions for its protein functionality is around 37 degrees Celsius (Jang et al. 2017). Meanwhile, *S. solfataricus* - a thermophile - has a proteome consisting of proteins, which have optimal conditions of 80 degrees Celsius (Zaparty et al. 2010).  The datasets consisted of 4392 and 2938 proteins for *E. coli* and *S. solfataricus* respectively. 

## Usage of protein embedding

Embedding is a technique to mapping from words to vectors, which allow to do a more convenient analysis in the model.

The protein embedding software `bio_embeddings` (Dallago et al. 2021) was chosen to accomplish this task for our case of protein sequences. The initial dataset of proteomes of two bacteria was prepocessed according to Basic Protocol 1: `config.yml` and `temperature_annotations.csv` files were created.

### Tasks to do

- [ ] Extract UniProt accession numbers from initial FASTA files.
- [ ] Create one FASTA file `training_sequences.fasta` that contains only UniProt accession numbers in the header.
- [ ] Create `temperature_annotations.csv` that contains identifier and temperature labels.
- [ ] Set up `config.yml` file to use the embedding.

## References

1. Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, 1, e113. doi: 10.1002/cpz1.113. https://currentprotocols.onlinelibrary.wiley.com/doi/10.1002/cpz1.113

2. Jang, J., Hur, H. G., Sadowsky, M. J., Byappanahalli, M. N., Yan, T., & Ishii, S. (2017). Environmental Escherichia coli: ecology and public health implications—a review. Journal of applied microbiology, 123(3), 570-581. https://sfamjournals.onlinelibrary.wiley.com/doi/full/10.1111/jam.13468

3. Zaparty, M., Esser, D., Gertig, S., Haferkamp, P., Kouril, T., Manica, A., ... & Siebers, B. (2010). “Hot standards” for the thermoacidophilic archaeon Sulfolobus solfataricus. Extremophiles, 14(1), 119-142. https://link.springer.com/article/10.1007/s00792-009-0280-0

