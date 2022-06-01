# Data for analysis of experimentally determined optimal temperature of
# the proteins

## Thermostable cellulases

DOI: 10.1016/j.biortech.2019.01.049

15 proteins were picked from the table 1 of the given article. Some
of the picked proteins had temperature of 60 or 65 degrees Celsius, 
therefore they were appropriate instances to check whether the classifier
works alright at the partition (or close) values. 

003 classifier is trained to distinguish two thermostability classes: 0-64
and 65-100 degrees Celsius.

None of the sequences was longer than 1022 amino acids.

## Hyperthermophilic enzymes

DOI: 10.1111/j.1742-4658.2007.05954.x

12 proteins were picked from the table 1 of the given article. 
All of the proteins belong to the thermostable class. However,
since the 003 classifier, which is currently (June 2022) included 
in `thermoclass` program, was trained on sequences that had temperature
label up to 100, it is interesting to check, whether sequences with 
optimal temperature above 100 will be classified correctly.

None of the sequences was longer than 1022 amino acids.

## Renaming sequence headers 

```
./scripts/experimental/rename_headers.sh data/experimental/10.1016_j.biortech.2019.01.049/FASTA/
./scripts/experimental/rename_headers.sh data/experimental/10.1111_j.1742-4658.2007.05954.x/FASTA/
```

Collecting sequences to one FASTA file:
```
cat data/experimental/10.1016_j.biortech.2019.01.049/FASTA/*.fasta > thermoclass/FASTA/10.1016_j.biortech.2019.01.049.fasta
cat data/experimental/10.1111_j.1742-4658.2007.05954.x/FASTA/*.fasta > thermoclass/FASTA/10.1111_j.1742-4658.2007.05954.x.fasta
```

## Making predictions

Mean predictions:
```
./thermoclass -f FASTA/10.1016_j.biortech.2019.01.049.fasta -g -c -e ./emb/ \
	-n ./emb/NPZ/10.1016_j.biortech.2019.01.049.npz -t ./emb/TSV/10.1016_j.biortech.2019.01.049.tsv \
	-o predictions/TSV/10.1016_j.biortech.2019.01.049.tsv

./thermoclass -f FASTA/10.1111_j.1742-4658.2007.05954.x.fasta -g -c -e ./emb/ \
    -n ./emb/NPZ/10.1111_j.1742-4658.2007.05954.x.npz -t ./emb/TSV/10.1111_j.1742-4658.2007.05954.x.tsv \
    -o predictions/TSV/10.1111_j.1742-4658.2007.05954.x.tsv
```

Output of the mean predictions:

seq_id binary_prediction raw_prediction
5087|Q0ZUL0|60  0       0.0026461154
5087|Q8TG37|65  0       0.0012982739
5087|Q96UI5|70  0       0.011200142
5528|O93782|80  0       0.021024736
5528|O93783|80  0       0.09290317
5528|P15828|55  0       0.003292402
5528|Q12622|60  0       0.17552578
68825|1Q9H|80   0       0.0013404206
68825|Q8TFL9|80 0       0.0008433439
68825|Q8TGI8|65 0       0.0016863742
83428|A0A0H4SHD0|75     0       0.38476336
209285|A3F8V2|70        0       0.017239733
209285|A7WNU1|65        0       0.0022070264
223376|A7WNT9|60        0       0.0021155523
575526|C5H6X3|75        1       0.6868626

seq_id binary_prediction raw_prediction
2261|Q9HHB3|105 1       0.9997603
2261|Q51733|105 1       0.99962294
2262|Q7LYT7|100 1       0.9995788
2337|O85251|103 1       0.9999119
46539|O93776|120        1       0.9985391
70601|O59196|100        1       0.99893314
110163|Q9P9A0|100       1       0.99958295
186497|E7FHL9|100       1       0.9998826
186497|P49067|106       1       0.9999987
186497|Q8U3L0|100       1       0.9999944
186497|Q8U259|100       1       0.9870848
555311|D0KQM8|120       1       0.99994683

Per-token predictions:
```
./thermoclass -f FASTA/10.1016_j.biortech.2019.01.049.fasta -g --per_tok -e ./emb/ \
    -n ./emb/NPZ/10.1016_j.biortech.2019.01.049-per-tok.npz -t ./emb/TSV/10.1016_j.biortech.2019.01.049-per-tok.tsv \
    -o predictions/TSV/10.1016_j.biortech.2019.01.049-per-tok.tsv \
	--output_fasta=predictions/FASTA/10.1016_j.biortech.2019.01.049-per-tok.fasta \
	--output_plot=predictions/PNG/10.1016_j.biortech.2019.01.049/

./thermoclass -f FASTA/10.1111_j.1742-4658.2007.05954.x.fasta -g --per_tok -e ./emb/ \
    -n ./emb/NPZ/10.1111_j.1742-4658.2007.05954.x-per-tok.npz -t ./emb/TSV/10.1111_j.1742-4658.2007.05954.x-per-tok.tsv \
    -o predictions/TSV/10.1111_j.1742-4658.2007.05954.x-per-tok.tsv \
	--output_fasta=predictions/FASTA/10.1111_j.1742-4658.2007.05954.x-per-tok.fasta \
	--output_plot=predictions/PNG/10.1111_j.1742-4658.2007.05954.x/
```

