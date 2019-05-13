import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

import requests

# preprocess.
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# dl libraraies
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam, SGD, Adagrad, Adadelta, RMSprop
from tensorflow.keras.utils import to_categorical

# specifically for cnn
from tensorflow.keras.layers import Dropout, Flatten, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization

from tensorflow.keras.callbacks import ReduceLROnPlateau

import random as rn

# specifically for manipulating zipped images and getting numpy arrays of pixel values of images.
import cv2
import numpy as np
from tqdm import tqdm
import os
from random import shuffle
from zipfile import ZipFile
from PIL import Image

node_status = 'http://127.0.0.1:3000/api/status'
py_reload = 'http://127.0.0.1:5000/reload'


class KCallback(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        update_status("Training Model", 0)

    def on_train_end(self, logs={}):
        reload_model()
        update_status("Finished", 0)

    def on_epoch_begin(self, epoch, logs={}):
        update_status("Training Model (Epoch " + str(epoch + 1) + "/" + str(epochs) + ")",
                      int(((epoch + 1) / epochs) * 100))
        return

    def on_epoch_end(self, epoch, logs={}):
        return

    def on_batch_begin(self, batch, logs={}):
        return

    def on_batch_end(self, batch, logs={}):
        return


X = []
Z = []
IMG_SIZE = 150


def assign_label(img, ranking):
    return ranking


def make_train_data(ranking, DIR):
    for img in tqdm(os.listdir(DIR)):
        label = assign_label(img, ranking)
        path = os.path.join(DIR, img)
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        X.append(np.array(img))
        Z.append(str(label))


def update_status(status, progress):
    requests.post(node_status, json={'status': status, 'progress': progress})


def reload_model():
    requests.get(py_reload)


RATE_1_DIR = './data/combined/1'
RATE_2_DIR = './data/combined/2'
RATE_3_DIR = './data/combined/3'
RATE_4_DIR = './data/combined/4'
RATE_5_DIR = './data/combined/5'

update_status("Preparing Model", 0)
make_train_data('1', RATE_1_DIR)
update_status("Preparing Model", 20)
make_train_data('2', RATE_2_DIR)
update_status("Preparing Model", 40)
make_train_data('3', RATE_3_DIR)
update_status("Preparing Model", 60)
make_train_data('4', RATE_4_DIR)
update_status("Preparing Model", 80)
make_train_data('5', RATE_5_DIR)
update_status("Preparing Model", 100)

le = LabelEncoder()
Y = le.fit_transform(Z)
Y = to_categorical(Y, 5)
X = np.array(X)
X = X / 255

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

# # modelling starts using a CNN.

tf.config.gpu.set_per_process_memory_fraction(0.4)

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Same', activation='relu', input_shape=(150, 150, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(filters=96, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(filters=96, kernel_size=(3, 3), padding='Same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dense(5, activation="softmax"))

batch_size = 128
epochs = 50

red_lr = ReduceLROnPlateau(monitor='val_acc', patience=3, verbose=1, factor=0.1)

datagen = ImageDataGenerator(
    featurewise_center=False,  # set input mean to 0 over the dataset
    samplewise_center=False,  # set each sample mean to 0
    featurewise_std_normalization=False,  # divide inputs by std of the dataset
    samplewise_std_normalization=False,  # divide each input by its std
    zca_whitening=False,  # apply ZCA whitening
    rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
    zoom_range=0.1,  # Randomly zoom image
    width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
    height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
    horizontal_flip=True,  # randomly flip images
    vertical_flip=False)  # randomly flip images

datagen.fit(x_train)

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

History = model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),
                              epochs=epochs, validation_data=(x_test, y_test),
                              verbose=1, steps_per_epoch=x_train.shape[0] // batch_size, callbacks=[KCallback()])

model.save("model.h5")

exit(0)
