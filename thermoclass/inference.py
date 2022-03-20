import numpy
import torch

# Loading embeddings to a dictionary with according keywords
# Example keywords: ['x_input', 'y_input']
def load_tensor_from_NPZ(NPZ_file, keywords):
    dataset = {}
    with numpy.load(NPZ_file, allow_pickle=True) as data_loaded:
        for i in range(len(keywords)):
            dataset[keywords[i]] = torch.from_numpy(data_loaded[keywords[i]])
    return dataset

# Making inferences about an unlabelled data
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
