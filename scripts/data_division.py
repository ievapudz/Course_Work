import sys
from Bio import SeqIO
from sklearn.model_selection import train_test_split

temperature_labels_full = [37, 80]

data = {
    'train': {
        'X' : [],
        'Y' : [],
        'prefix': 'training_'
    },
    'validate': {
        'X' : [],
        'Y' : [],
        'prefix': 'validation_'
    },
    'test': {
        'X' : [],
        'Y' : [],
        'prefix': 'testing_'
    }
}

for i in range(len(temperature_labels_full)):
    records = [] 
    # Parsing sequences (X dataset) from one dataset 
    for record in SeqIO.parse(sys.argv[i+1], "fasta"):
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
