import sys
import statistics
import math

# Preparing kmers results to be printed in FASTA format.
def get_kmers_results_as_FASTA(input_file_name, sep, headerless, output_file_name, 
                               include_min, include_max, include_mean, include_median, include_std):
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
            sequences[line_arr[0]]['predictions'] = []
        else:
            sequences[line_arr[0]]['label_seq'] += line_arr[2]
         
        sequences[line_arr[0]]['predictions'].append(float(line_arr[3]))

    file_handle.close()
   
    file_handle = open(output_file_name, 'w')

    for seq in sequences.keys():

       if(seq == 'Cas'):
           print(sequences[seq])

       line_to_write = '>'+seq
       if(len(sequences[seq]['predictions']) < 2):
           continue 
       if(include_min):
           minimum = min(sequences[seq]['predictions'])
           line_to_write += "\t"+'min='+str(minimum)
       if(include_max):
           maximum = max(sequences[seq]['predictions'])
           line_to_write += "\t"+'max='+str(maximum)
       if(include_mean):
           mean = get_kmers_predictions_mean(sequences, seq)
           line_to_write += "\t"+'mean='+str(mean)
       if(include_median):
           median = statistics.median(sequences[seq]['predictions'])
           line_to_write += "\t"+'median='+str(median)
       if(include_std):
           std = statistics.stdev(sequences[seq]['predictions'])
           line_to_write += "\t"+'std='+str(std)

       file_handle.write(line_to_write+"\n"+sequences[seq]['label_seq']+"\n")
    file_handle.close()

# Calculating the average class prediction for the sequence.
def get_kmers_predictions_mean(seq_dict, seq_key):
    predictions_sum = 0

    for pred in seq_dict[seq_key]['predictions']:
        predictions_sum += pred

    mean = predictions_sum / len(seq_dict[seq_key]['label_seq'])

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
    if(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)) == 0):
        print(sys.argv[0]+": division by 0 at threshold "+str(prediction_threshold), file=sys.stderr)
    else:
        MCC = (TP*TN-FP*FN)/(math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
        return MCC
