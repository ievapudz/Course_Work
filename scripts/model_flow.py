import torch
from torch import nn
from sklearn import metrics
import torch
import matplotlib.pyplot as plt
import numpy

def train_epoch(model, trainloader, loss_function, optimizer, batch_size, epoch_batch_size, epoch):
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
        
        # Perform backward pass
        loss.backward()
        
        # Perform optimization
        optimizer.step()
        
        # Print statistics
        current_loss += loss.item()
        if i % batch_size == (batch_size-1):
            print('Loss after mini-batch %5d: %.3f' %
                  (i + 1, current_loss / batch_size))
            current_loss = 0.0
        #if i == epoch_batch_size:
        #    plot_ROC_curve(targets, outputs, './results/SLP/ROC/training_'+str(epoch)+'_'+str(i)+'.png')

def validation_epoch(model, validateloader, loss_function, batch_size, epoch_batch_size, epoch, ROC_curve_plot_file_dir='./results/'):
    current_loss = 0.0 

    # Iterate over the DataLoader for training data
    for i, data in enumerate(validateloader, 0):
        # Get inputs
        inputs, targets = data
        targets = targets.reshape(batch_size, 1)
        targets = targets.to(torch.float32)
        
        # Compute loss
        outputs = model(inputs)
        
        # Print statistics
        loss = loss_function(outputs, targets)
        outputs = outputs.detach().numpy()

        current_loss += loss.item()
        if i % batch_size == (batch_size-1):
            print('Validation loss after mini-batch %5d: %.3f' %
                  (i + 1, current_loss / batch_size))
            current_loss = 0.0
        if i == epoch_batch_size:
            plot_ROC_curve(targets, outputs, ROC_curve_plot_file_dir+'validation_'+str(epoch)+'_'+str(i)+'.png')

def plot_ROC_curve(targets, outputs, fig_name):
    # A function that plots ROC curve
    fpr, tpr, _ = metrics.roc_curve(targets, outputs)
    plt.plot(fpr,tpr)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig(fig_name)
    
    
    
    
