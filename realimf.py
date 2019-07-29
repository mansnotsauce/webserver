# -*- coding: utf-8 -*-
"""
Created on Mon May 13 16:59:17 2019

@author: MBaer
"""

from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy as np
import tensorflow_hub as hub#this

def run():
    data_root = "C:/Users/MBaer/Desktop/webserver/Images"
    saved_model = "C:/Users/MBaer/Desktop/imf/savedmodel"
    feature_extractor_url = "https://tfhub.dev/google/imagenet/resnet_v2_152/feature_vector/1"#this
    
    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
    IMAGE_SIZE = [224, 224]
    
    image_data = image_generator.flow_from_directory(data_root, target_size=IMAGE_SIZE)
    
    model = tf.contrib.saved_model.load_keras_model(saved_model)
    #model = tf.keras.models.load_model(saved_model)
    
    import tensorflow.keras.backend as K
    sess = K.get_session()
    init = tf.global_variables_initializer()
    sess.run(init)
    
    model.compile(optimizer=tf.train.AdamOptimizer(), loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    result_data = model.predict(image_data)
    
    label_names = ['Pass', 'Fail']
    label_names = np.array(label_names, dtype='<U10')
    
    predictions = label_names[np.argmax(result_data, axis=-1)]
    return(predictions[0])
