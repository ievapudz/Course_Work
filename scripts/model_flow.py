import torch
from torch import nn
from sklearn import metrics
import torch
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy

def train_epoch(model, trainloader, loss_function, optimizer, batch_size, 
                epoch_batch_size, epoch, print_predictions=False,
                print_loss=True):
    # Set current loss value
    current_loss = 0.0
    
    # Iterate over the DataLoader for training data
    for i, data in enumerate(trainloader, 0):
        # Get inputs
        inputs, targets = data
        targets = targets.reshape(batch_size, 1)
        targets = targets.to(torch.float32)
        
        # Zero the gradients
        optimizer.zero_grad()
        
        # Perform forward pass
        outputs = model(inputs)
        
        # Compute loss
        loss = loss_function(outputs, targets)
        outputs = outputs.detach().numpy()
        
        # Printing prediction values
        if(print_predictions):
            for output in outputs:
                print(output)
        
        # Perform backward pass
        loss.backward()
        
        # Perform optimization
        optimizer.step()
        
        # Print statistics
        current_loss += loss.item()
        if i % batch_size == (batch_size-1):
            if(print_loss):
                print('Loss after mini-batch %5d: %.3f' %
                      (i + 1, current_loss / batch_size))
            current_loss = 0.0

def validation_epoch(model, validateloader, loss_function, batch_size, 
		     epoch_batch_size, num_of_epochs, epoch, 
                     ROC_curve_plot_file_dir='./results/', 
                     confusion_matrix_file_dir='',
                     print_predictions=False, print_loss=True):
    current_loss = 0.0 

    tensor_list = []
    epoch_outputs = []
    # Iterate over the DataLoader for training data
    for i, data in enumerate(validateloader, 0):
        # Get inputs
        inputs, targets = data
        targets = targets.reshape(batch_size, 1)
        targets = targets.to(torch.float32)
        
        # Compute loss
        outputs = model(inputs)
        
        # Printing prediction values
        if(print_predictions):
            for index, output in enumerate(outputs):
                print(targets[index].item(), output.item())

        # Print statistics
        loss = loss_function(outputs, targets)
        outputs = outputs.detach().numpy()

        epoch_outputs.append(outputs)
        tensor_list.append(targets)

        current_loss += loss.item()
        if i % batch_size == (batch_size-1):
            if(print_loss):
                print('Validation loss after mini-batch %5d: %.3f' %
                  (i + 1, current_loss / batch_size))
            current_loss = 0.0
            
    epoch_targets = torch.cat(tensor_list, dim = 0)
    if ROC_curve_plot_file_dir != '':
        if epoch == num_of_epochs-1:
            plot_ROC_curve(epoch_targets, num_of_epochs,
                               numpy.array(epoch_outputs).flatten(),
                               ROC_curve_plot_file_dir+'validation_'+
                               str(epoch)+'_'+str(i)+'.png', True)
        else:
            plot_ROC_curve(epoch_targets, num_of_epochs, 
			       numpy.array(epoch_outputs).flatten(), 
			       ROC_curve_plot_file_dir+'validation_'+
			       str(epoch)+'_'+str(i)+'.png')
          
    if confusion_matrix_file_dir != '':
        create_confusion_matrix(epoch_targets, epoch_outputs, 
                                confusion_matrix_file_dir+
                                'validation_'+str(epoch)+'_'+
                                str(i)+'.txt')

def plot_ROC_curve(targets, num_of_epochs, outputs, fig_name, clear_plot=False):
    # A function that plots ROC curve
    fpr, tpr, _ = metrics.roc_curve(targets, outputs)
    iterated_colors = [plt.get_cmap('jet')(1. * i/num_of_epochs) for i in range(num_of_epochs)]
    mpl.rcParams['axes.prop_cycle'] = cycler('color', iterated_colors)
    plt.plot(fpr,tpr)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(fig_name)
    if clear_plot:
        plt.clf()
    
def create_confusion_matrix(targets, outputs, file_path=''):
    # targets - 1D tensor
    # outputs - list of model predictions (probabilities).

    #Predicted  0    1
    #Actual         
    #0          TN  FP
    #1          FN  TP

    predicted_labels = []
    for output in numpy.array(outputs).flatten():
        if output >= 0.5:
            predicted_labels.append(1)
        else:
            predicted_labels.append(0)

    confusion_matrix = metrics.confusion_matrix(targets.tolist(), predicted_labels)
    result = "\t0\t1\n0\t{0}\t{1}\n1\t{2}\t{3}\n".format(confusion_matrix[0][0], 
                                                        confusion_matrix[0][1], 
                                                        confusion_matrix[1][0], 
                                                        confusion_matrix[1][1])
    scores = "Accuracy:\t{0}\nPrecision:\t{1}\nRecall:\t{2}\nArea under the curve:\t{3}".format(metrics.accuracy_score(targets.tolist(), predicted_labels),
                                                                    metrics.precision_score(targets.tolist(), predicted_labels),
                                                                    metrics.recall_score(targets.tolist(), predicted_labels),
								    metrics.roc_auc_score(targets.tolist(), predicted_labels))
    
    if file_path == '':
        print(result, scores)
    else:
        with open(file_path, 'w') as file_handle:
            file_handle.write(result)
            file_handle.write(scores)
    
def test_epoch(model, test_loader, batch_size, prefix='testing_0_', 
               ROC_curve_plot_file_dir='./results/',
               confusion_matrix_file_dir='', 
               file_for_predictions='', print_true_labels=True):

    tensor_list = []
    epoch_outputs = []

    if(file_for_predictions != ''):
        file_handle = open(file_for_predictions, 'w')
    
    # Iterate over the DataLoader for testing data
    for i, data in enumerate(test_loader, 0):
        # Get inputs
        inputs, targets = data
        #targets = targets.reshape(batch_size, 1)
        targets = targets.to(torch.float32)

        # Perform forward pass
        outputs = model(inputs)

        # Compute loss
        outputs = outputs.detach().numpy()

        epoch_outputs.append(outputs)
        tensor_list.append(targets)

        # Printing prediction values
        for index, output in enumerate(outputs):
            if(print_true_labels):
                file_handle.write(str(targets[index].item())+"\t"+str(output.item())+"\n")
            else:
                file_handle.write(str(output.item())+"\n")

    epoch_targets = torch.cat(tensor_list, dim = 0)
    if ROC_curve_plot_file_dir != '':
        plot_ROC_curve(epoch_targets, 1,
                   numpy.array(epoch_outputs).flatten(),
                   ROC_curve_plot_file_dir+prefix+
                   str(i)+'.png', True)
    
    if confusion_matrix_file_dir != '':
        create_confusion_matrix(epoch_targets, epoch_outputs,
                                confusion_matrix_file_dir+
                                prefix+
                                str(i)+'.txt')

    file_handle.close()

# A function that makes inferences about unlabelled data
def unlabelled_test_epoch(model, test_loader, threshold, 
                          file_for_predictions='', binary_predictions_only=True):
    
    epoch_outputs = []

    if(file_for_predictions != ''):
        file_handle = open(file_for_predictions, 'w')

    # Iterate over the DataLoader for testing data
    for i, data in enumerate(test_loader, 0):
        inputs, targets = data
        outputs = model(inputs)
        outputs = outputs.detach().numpy()
        epoch_outputs.append(outputs)
        
         # Printing prediction values
        for output in outputs:
            if(binary_predictions_only):
                if(output[0] >= threshold):
                    file_handle.write("1\n")
                else:
                    file_handle.write("0\n")
            else:
                if(output[0] >= threshold):
                    file_handle.write("1\t"+str(output[0])+"\n")
                else:
                    file_handle.write("0\t"+str(output[0])+"\n")

    file_handle.close()

# Calculation of prediction's accuracy per organism 
def calculate_accuracy_per_tax_id(predictions_dict, out_filename=''):
    
    if(out_filename != ''):
        file_handle = open(out_filename, 'w')
        file_handle.write("TaxID\ttrue_temperature\tperc_0\tperc_1\n")
    else:
        print("TaxID\ttrue_temperature\tperc_0\tperc_1")

    for taxid in predictions_dict.keys():
        all_predictions = predictions_dict[taxid]['0'] + \
                          predictions_dict[taxid]['1']
        predicted_0_percentage = predictions_dict[taxid]['0'] / \
                                 all_predictions * 100
        predicted_1_percentage = predictions_dict[taxid]['1'] / \
                                 all_predictions * 100
        if(out_filename != ''):
            file_handle.write('{}\t{}\t{}\t{}\n'.format(taxid, predictions_dict[taxid]['true_temperature'],
                              predicted_0_percentage, predicted_1_percentage))
        else:
            print('{}\t{}\t{}\t{}'.format(taxid, predictions_dict[taxid]['true_temperature'], 
                              predicted_0_percentage, predicted_1_percentage))

    if(out_filename != ''):
        file_handle.close()

