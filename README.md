# CARE ver 1.0
Gesture recognition for hospital environments via CNN neural network implemented in Keras + Theano + OpenCV


Key Requirements:
Python 2.7.13
OpenCV 2.4.8
Keras 2.0.2
Theano 0.9.0

Suggestion: Better to download Anaconda as it will take care of most of the other packages and easier to setup a virtual workspace to work with multiple versions of key packages like python, opencv etc.


# Repo contents
- **trackgesture.py** : The main script launcher. This file contains all the code for UI options and OpenCV code to capture camera contents. This script internally calls interfaces to gestureCNN.py.
- **gestureCNN.py** : This script file holds all the CNN specific code to create CNN model, load the weight file (if model is pretrained), train the model using image samples present in **./imgfolder_b**, visualize the feature maps at different layers of NN (of pretrained model) for a given input image present in **./imgs** folder.
- **imgfolder_b** : This folder contains all the 4015 gesture images I took in order to train the model.
- **_ori_4015imgs_weights.hdf5_** : This is pretrained file. If for some reason you find issues with downloading from github then it can be downloaded from my google driver link - https://drive.google.com/open?id=0B6cMRAuImU69SHNCcXpkT3RpYkE
- **_imgs_** - This is an optional folder of few sample images that one can use to visualize the feature maps at different layers. These are few sample images from imgfolder_b only.
- **_ori_4015imgs_acc.png_** : This is just a pic of a plot depicting model accuracy Vs validation data accuracy after I trained it.
- **_ori_4015imgs_loss.png_** : This is just a pic of a plot depicting model loss Vs validation loss after I training.

# Usage
```bash
$ KERAS_BACKEND=theano python trackgesture.py 
```
We are setting KERAS_BACKEND to change backend to Theano, so in case you have already done it via Keras.json then no need to do that. But if you have Tensorflow set as default then this will be required.
