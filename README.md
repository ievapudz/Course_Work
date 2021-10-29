# Protein Classificator

## Prerequisites

- Python3 (tested on Python 3.7.4)

## Primary dataset for training

Firstly, proteomes of *Escherichia coli* (https://www.uniprot.org/proteomes/UP000000625) and *Sulfolobus solfataricus* (https://www.uniprot.org/proteomes/UP000001974) were taken to train the model. Due to the growth conditions of each organism, *E. coli* was taken as a representative of mesophiles, assuming that the optimal conditions for its protein functionality is around 37 degrees Celsius (Jang et al. 2017). Meanwhile, *S. solfataricus* - a thermophile - has a proteome consisting of proteins, which have optimal conditions of 80 degrees Celsius (Zaparty et al. 2010).  The datasets consisted of 4392 and 2938 proteins for *E. coli* and *S. solfataricus* respectively. 

## Usage of protein embedding

Embedding is a technique to mapping from words to vectors, which allow to do a more convenient analysis in the model.

The protein embedding software `bio_embeddings` (Dallago et al. 2021) was chosen to accomplish this task for our case of protein sequences. The initial dataset of proteomes of two bacteria was prepocessed according to Basic Protocol 1: `config.yml` and `temperature_annotations.csv` files were created.

## Removal of duplicated sequences

Initially generated sequences files were not taken as input to the 
embedding tool, since FASTA file included several sequences that had duplicates by the sequence.

Repeated sequences from `training_sequences.fasta` file:

>P0CE49
>P0CE51
>P0CE52
>P0CE54
>P0CE55
>P0CE58
MSHQLTFADSEFSSKRRQTRKEIFLSRMEQILPWQNMVEVIEPFYPKAGNGRRPYPLETMLRIHCMQHWYNLSDGAMEDALYEIASMRLFARLSLDSALPDRTTIMNFRHLLEQHQLARQLFKTINRWLAEAGVMMTQGTLVDATIIEAPSSTKNKEQQRDPEMHQTKKGNQWHFGMKAHIGVDAKSGLTHSLVTTAANEHDLNQLGNLLHGEEQFVSADAGYQGAPQREELAEVDVDWLIAERPGKVRTLKQHPRKNKTAINIEYMKASIRARVEHPFRIIKRQFGFVKARYKGLLKNDNQLAMLFTLANLFRADQMIRQWERSH

>P0CF53
>P0CF54
>P0CF56
>P0CF57
>P0CF58
MDSARALIARGWGVSLVSRCLRVSRAQLHVILRRTDDWMDGRRSRHTDDTDVLLRIHHVIGELPTYGYRRVWALLRRQAELDGMPAINAKRVYRIMRQNALLLERKPAVPPSKRAHTGRVAVKESNQRWCSDGFEFCCDNGERLRVTFALDCCDREALHWAVTTGGFNSETVQDVMLGAVERRFGNDLPSSPVEWLTDNGSCYRANETRQFARMLGLEPKNTAVRSPESNGIAESFVKTIKRDYISIMPKPDGLTAAKNLAEAFEHYNEWHPHSALGYRSPREYLRQRACNGLSDNRCLEI

>P0CF40
>P0CF41
>P0CF44
>P0CF45
MIDVLGPEKRRRRTTQEKIAIVQQSFEPGMTVSLVARQHGVAASQLFLWRKQYQEGSLTAVAAGEQVVPASELAAAMKQIKELQRLLGKKTMENELLKEAVEYGRAKKWIAHAPLLPGDGE

>P0CF67
>P0CF69
>P0CF70
MTKTVSTSKKPRKQHSPEFRSEALKLAERIGVTAAARELSLYESQLYNWRSKQQNQQTSSERELEMSTEIARLKRQLAERDEELAILQKAATYFAKRLK

>A0A385XJL4
>P0CF25
>P0CF28
MPGNSPHYGRWPQHDFTSLKKLRPQSVTSRIQPGSDVIVCAEMDEQWGYVGAKSRQRWLFYAYDSLRKTVVAHVFGERTMATLGRLMSLLSPFDVVIWMTDGWPLYESRLKGKLHVISKRYTQRIERHNLNLRQHLARLGRKSLSFSKSVELHDKVIGHYLNIKHYQ

>P0CF79
>P0CF81
>P0CF82
MKYVFIEKHQAEFSIKAMCRVLRVARSGWYTWCQRRTRISTRQQFRQHCDSVVLAAFTRSKQRYGAPRLTDELRAQGYPFNVKTVAASLRRQGLRAKASRKFSPVSYRAHGLPVSENLLEQDFYASGPNQKWAGDITYLRTDEGWLYLAVVIDLWSRAVIGWSMSPRMTAQLACDALQMALWRRKRPRNVIVHTDRGGQYCSADYQAQLKRHNLRGSMSAKGCCYDNACVESFFHSLKVECIHGEHFISREIMRATVFNYIECDYNRWRRHSWCGGLSPEQFENKNLA

>P0CF26
>P0CF27
MPGNRPHYGRWPQHDFPPFKKLRPQSVTSRIQPGSDVIVCAEMDEQWGYVGAKSRQRWLFYAYDRLRKTVVAHVFGERTMATLGRLMSLLSPFDVVIWMTDGWPLYESRLKGKLHVISKRYTQRIERHNLNLRQHLARLGRKSLSFSKSVEQHDKVIGHYLNIKHYQ

>P0CF09
>P0CF10
MASVSISCPSCSATDGVVRNGKSTAGHQRYLCSHCRKTWQLQFTYTASQPGTHQKIIDMAMNGVGCRATARIMGVGLNTIFRHLKNSGRSR

### Tasks to do

- [x] Extract UniProt accession numbers from initial FASTA files.
- [x] Create FASTA files `*_sequences.fasta` which records contain only UniProt accession numbers in the header.
- [x] Create `*_temperature_annotations.csv` files that contain identifier and temperature labels.
- [x] Set up `config.yml` file to use the embedding.

## References

1. Dallago, C., Schütze, K., Heinzinger, M., Olenyi, T., Littmann, M., Lu, A. X., Yang, K. K., Min, S., Yoon, S., Morton, J. T., & Rost, B. (2021). Learned embeddings from deep learning to visualize and predict protein sets. Current Protocols, 1, e113. doi: 10.1002/cpz1.113. https://currentprotocols.onlinelibrary.wiley.com/doi/10.1002/cpz1.113

2. Jang, J., Hur, H. G., Sadowsky, M. J., Byappanahalli, M. N., Yan, T., & Ishii, S. (2017). Environmental Escherichia coli: ecology and public health implications—a review. Journal of applied microbiology, 123(3), 570-581. https://sfamjournals.onlinelibrary.wiley.com/doi/full/10.1111/jam.13468

3. Zaparty, M., Esser, D., Gertig, S., Haferkamp, P., Kouril, T., Manica, A., ... & Siebers, B. (2010). “Hot standards” for the thermoacidophilic archaeon Sulfolobus solfataricus. Extremophiles, 14(1), 119-142. https://link.springer.com/article/10.1007/s00792-009-0280-0

