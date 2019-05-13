import os
import cv2
from tqdm import tqdm
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model

tf.config.gpu.set_per_process_memory_fraction(0.65)

IMG_SIZE = 150
X = []
RATE_5_DIR = './data/combined/4'
imgs = []


def make_train_data(DIR):
    [imgs.append(i) for i in os.listdir(DIR)]
    for img in tqdm(os.listdir(DIR)):
        path = os.path.join(DIR, img)
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        X.append(np.array(img))


model = load_model('model.h5')

make_train_data(RATE_5_DIR)

X = np.array(X)
X = X / 255

YZ = model.predict_classes(X)

for idx, i in enumerate(YZ):
    print(imgs[idx] + ": " + str(i))
