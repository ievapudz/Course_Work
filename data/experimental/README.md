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
