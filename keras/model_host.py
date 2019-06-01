import io
import os
import cv2
import flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import imagehash
import subprocess

app = flask.Flask(__name__)

# tf.config.gpu.set_per_process_memory_fraction(0.65)

model = None

IMG_SIZE = 150


def do_load_model():
    with tf.device('/cpu:0'):
        global model
        model = load_model('model.h5')


do_load_model()


def get_extension(format):
    if format == 'JPEG':
        return "jpg"
    if format == 'PNG':
        return "png"
    return "DUNNO"


def find_duplicate(hash):
    DIR = "./data/combined"

    level = []
    files = []

    for folder in os.listdir(DIR):
        for img in os.listdir(DIR + "/" + folder):
            files.append(img)
            level.append(folder)

    if hash in files:
        return int(level[files.index(hash)])

    return 0


def to_pimg(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    return Image.open(in_memory_file)


def load_mem(file):
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    return in_memory_file


training = False
proc = None

import os


@app.route("/retrain", methods=["GET"])
def retrain():
    global training
    if not training:
        training = True
        global proc
        dirpath = os.getcwd()
        proc = subprocess.Popen([dirpath + "/venv/Scripts/python.exe", "train.py"], shell=True,
                                stdin=None, stdout=None, stderr=None, close_fds=True)
        return flask.jsonify({"success": True})
    else:
        return flask.jsonify({"success": False})


@app.route("/forcetrain", methods=["GET"])
def forcetrain():
    global training
    training = False
    return flask.jsonify({"success": True})


@app.route("/reload", methods=["GET"])
def reload():
    global training
    training = False
    do_load_model()
    return flask.jsonify({"success": True})


@app.route("/predict", methods=["POST"])
def predict():
    res = {"success": False}
    if 'photo' in flask.request.files:
        photo = flask.request.files['photo']
        mf = load_mem(photo)
        pimg = Image.open(mf)
        hash = imagehash.average_hash(pimg)
        duplicate = find_duplicate(str(hash) + "." + get_extension(pimg.format))
        if duplicate > 0:
            res['predict'] = duplicate
            res['success'] = True
            res['fromCache'] = True
        else:
            X = []
            mf.seek(0)
            data = np.asarray(bytearray(mf.read()), dtype=np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            X.append(np.array(img))

            X = np.array(X)
            X = X / 255
            with tf.device('/cpu:0'):
                pred = model.predict_classes(X)[0]
                res['predict'] = int(pred) + 1
            res['fromCache'] = False
            res['success'] = True

    return flask.jsonify(res)


@app.route("/add", methods=["POST"])
def add_to_model():
    res = {"success": False, "move": False}

    if 'rank' in flask.request.form and 'photo' in flask.request.files:
        photo = flask.request.files['photo']
        rank = str(flask.request.form['rank'])
        pimg = to_pimg(photo)
        hash = imagehash.average_hash(pimg)
        res['hash'] = str(hash)
        duplicate = find_duplicate(str(hash) + "." + get_extension(pimg.format))
        if duplicate > 0:
            res['move'] = True
            res['from'] = duplicate
            os.rename('./data/combined/' + str(duplicate) + "/" + str(hash) + "." + get_extension(pimg.format),
                      './data/combined/' + rank + "/" + str(hash) + "." + get_extension(pimg.format))
        else:
            pimg.save('./data/combined/' + rank + "/" + str(hash) + "." + get_extension(pimg.format))

        res['success'] = True
    return flask.jsonify(res)


app.run(host="0.0.0.0")
