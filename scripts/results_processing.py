import math

# Preparing kmers results to be printed in FASTA format.
def get_kmers_results_as_FASTA(input_file_name, sep, headerless, output_file_name, include_mean):
    file_handle = open(input_file_name, 'r')
    
    sequences = {} 
    while True:
    
        line = file_handle.readline()
      
        if not line:
            break
        
        line = line.rstrip()
        line_arr = line.split(sep)
      
        if(line_arr[0] not in sequences.keys()):
            sequences[line_arr[0]] = {}
            sequences[line_arr[0]]['label_seq'] = line_arr[2]
            sequences[line_arr[0]]['predictions_sum'] = 0
        else:
            sequences[line_arr[0]]['label_seq'] += line_arr[2]
         
        sequences[line_arr[0]]['predictions_sum'] += float(line_arr[3])

    file_handle.close()
    
    file_handle = open(output_file_name, 'w')

    for seq in sequences.keys():
       if(include_mean):
           mean = get_kmers_predictions_mean(sequences, seq)
           file_handle.write('>'+seq+"\t"+str(mean)+"\n"+sequences[seq]['label_seq']+"\n")
       else:
           file_handle.write('>'+seq+"\n"+sequences[seq]['label_seq']+"\n")
    
    file_handle.close()

# Calculating the average class prediction for the sequence.
def get_kmers_predictions_mean(seq_dict, seq_key):
    mean = seq_dict[seq_key]['predictions_sum'] / \
           len(seq_dict[seq_key]['label_seq'])

    return mean

# A function that calculates Matthew's correlation coefficient
def calculate_MCC(real, prediction, real_threshold=0.65, 
                  prediction_threshold=0.5):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i, el in enumerate(real):
        if float(el) >= real_threshold and float(prediction[i]) >= prediction_threshold:
            TP += 1
        if float(el) < real_threshold and float(prediction[i]) < prediction_threshold:
            TN += 1
        if float(el) < real_threshold and float(prediction[i]) >= prediction_threshold:
            FP += 1
        if float(el) >= real_threshold and float(prediction[i]) < prediction_threshold:
            FN += 1
    MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
    return MCC
