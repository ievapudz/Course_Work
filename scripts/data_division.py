import sys
from Bio import SeqIO
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

"""
Requirements:
* biopython
* data.zip file that contains default proteomes
"""

# Configuration
temperature_labels_full = [37, 80]
files = []

if(sys.argv[1] == '-f'):
    # If the script is run in Colab environment
    files = ['data/proteomes/UP000000625_83333.fasta', 'data/proteomes/UP000001974_273057.fasta']
elif(sys.argv == ''):
    # If the script is run as a part of UNIX pipeline, but no arguments were provided
    files = ['data/proteomes/UP000000625_83333.fasta', 'data/proteomes/UP000001974_273057.fasta']
else:
    # If the script is run as a part of UNIX pipeline with arguments
    files = sys.argv[1:]

# Initialisation of the dataset container
data = {
    'train': {
        'X' : [],
        'Y' : [],
        'FASTA_prefix': 'data/FASTA/training_',
        'CSV_prefix': 'data/CSV/training_',
    },
    'validate': {
        'X' : [],
        'Y' : [],
        'FASTA_prefix': 'data/FASTA/validation_',
        'CSV_prefix': 'data/CSV/validation_'
    },
    'test': {
        'X' : [],
        'Y' : [],
        'FASTA_prefix': 'data/FASTA/testing_',
        'CSV_prefix': 'data/CSV/testing_'
    }
}

# Removing duplicate sequences in the dataset
seen = set()
for i in range(len(temperature_labels_full)):
    records = [] 
    # Parsing sequences (X dataset) from one dataset 
    for record in SeqIO.parse(files[i], "fasta"):
        records.append(record)

    # Creating Y dataset from temperature labels 
    temperature_labels = [temperature_labels_full[i]] * len(records)

    # Spliting the dataset to 70% (training) and 30% (trying)
    X_train, X_try, Y_train, Y_try = train_test_split(records, temperature_labels, test_size=0.3, shuffle=True, random_state=1)

    # Splitting 30% from the initial set in half for calidation and testing
    X_validate, X_test, Y_validate, Y_test = train_test_split(X_try, Y_try, test_size=0.5, shuffle=True, random_state=1)

    data['train']['X'] = data['train']['X'] + X_train
    data['train']['Y'] = data['train']['Y'] + Y_train
    data['validate']['X'] = data['validate']['X'] + X_validate
    data['validate']['Y'] = data['validate']['Y'] + Y_validate
    data['test']['X'] = data['test']['X'] + X_test
    data['test']['Y'] = data['test']['Y'] + Y_test

print(len(data['train']['X']))
print(len(data['validate']['X']))
print(len(data['test']['X']))

# Shuffling the datasets
for element in data.keys():
    data[element]['X'], data[element]['Y'] = shuffle(data[element]['X'], data[element]['Y'], random_state=1)