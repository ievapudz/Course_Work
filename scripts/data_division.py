import sys
from Bio import SeqIO
from sklearn.model_selection import train_test_split

temperature_labels_full = [37, 80]

X_train_full = []
Y_train_full = []
X_validate_full = []
Y_validate_full = []
X_test_full = []
Y_test_full = []

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

    X_train_full = X_train_full + (X_train)
    Y_train_full = Y_train_full + (Y_train)
    X_validate_full = X_validate_full + (X_validate)
    Y_validate_full = Y_validate_full + (Y_validate)
    X_test_full = X_test_full + (X_test)
    Y_test_full = Y_test_full + (Y_test)

print(len(X_train_full))
print(len(X_validate_full))
print(len(X_test_full))


