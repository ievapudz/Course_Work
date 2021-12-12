import torch
from torch import nn

def train_epoch(model, trainloader, loss_function, optimizer, batch_size):
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

def validation_epoch(model, validateloader, loss_function, batch_size):
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
        
        current_loss += loss.item()
        if i % batch_size == (batch_size-1):
            print('Validation loss after mini-batch %5d: %.3f' %
                  (i + 1, current_loss / batch_size))
            current_loss = 0.0
