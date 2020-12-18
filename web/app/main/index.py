from flask import Blueprint, request, render_template, flash, redirect, url_for, make_response, send_file
from flask import current_app as app
import requests
import base64
import json
import numpy as np
from datetime import datetime
from PIL import Image
import os
import pickle
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

main = Blueprint('main', __name__, url_prefix='/')

target_size = 256
max_seq_length, n_chars, output_dict, output_chars = pickle.load(open('seqlen_nchar_outdict_outchar.pkl', 'rb'))
use_hashtag = pickle.load(open('usehash.pkl', 'rb'))

with tf.device('/gpu:0'):
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                            log_device_placement=True))
    sess2 = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                                            log_device_placement=True))
saver = tf.train.import_meta_graph('ver15.meta')
saver.restore(sess, 'ver15')
saver2 = tf.train.import_meta_graph('ver16.meta')
saver2.restore(sess2, 'ver16')

@main.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

@main.route('/translate', methods=['POST'])
def translate_image():
    if request.method == 'POST':
        f = request.files['file']
        filename = 'img_%s.jpg' %datetime.now().strftime('%Y%m%d_%H%M%S')
        path = 'app/static/images/%s' %filename
        f.save(path)
        return render_template('/main/index.html', filename=filename, get_sentence_result=get_sentence_result, get_hashtag_result=get_hashtag_result)

def get_image_from_path(path):
    image = Image.open(path)
    size = image.size

    if size[0] <= size[1]:
        scaled_size = (target_size, int(size[1]/size[0]*target_size))
        crop_area = (0, int((scaled_size[1]-target_size)/2), target_size, int((scaled_size[1]+target_size)/2))
    else:
        scaled_size = (int(size[0]/size[1]*target_size), target_size)
        crop_area = (int((scaled_size[0]-target_size)/2), 0, int((scaled_size[0]+target_size)/2), target_size)

    image = image.resize(scaled_size)
    image = image.crop(crop_area)
    return image

def get_array_from_path(path):
    return np.asarray(get_image_from_path(path))

def get_sentence_result(filename):
    path = 'app/static/images/%s' %filename
    image = get_array_from_path(path)
    return translate(image[:,:,:3])

def get_hashtag_result(filename):
    path = 'app/static/images/%s' %filename
    image = get_array_from_path(path)
    return translate2(image[:,:,:3])

def translate(image):
    dec_inp = np.zeros(shape=(1, max_seq_length, n_chars), dtype='float32')
    dec_inp[0,0,output_dict['\t']] = 1.
    result = sess.run('dense/BiasAdd:0',
                      feed_dict={'Placeholder:0': [image],
                                 'Placeholder_1:0': dec_inp})
    result = np.argmax(result, axis=2)
    decoded = [output_chars[i] for i in result[0]]
    end = decoded.index('\n') if '\n' in decoded else len(decoded)
    translated = ''.join(decoded[:end])
    return translated

def translate2(image):
    result = sess2.run('hashtag/dense_3/BiasAdd:0',
                       feed_dict={'Placeholder:0': [image]})[0]
    return ' '.join(use_hashtag[[i for i,p in enumerate(result) if p > 0.01]])

@main.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename), code=301)
