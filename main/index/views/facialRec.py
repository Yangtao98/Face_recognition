import cv2
import os
import random
import numpy as np

import math

from keras.models import Sequential, load_model

# Import tensorflow depenencies - Funcitonal API
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Layer, Conv2D, Dense, MaxPooling2D, Input, Flatten
import tensorflow as tf

# Import uuid library to generate unique image names
import uuid

# Import metric calculations
from tensorflow.keras.metrics import Precision, Recall



# Siamese L1 Distance class
class L1Dist(Layer):
	
	# Init method - inheritance
	def __init__(self, **kwargs):
		super().__init__()
       
	# Magic happens here - similarity calculation
	def call(self, input_embedding, validation_embedding):
		return tf.math.abs(input_embedding - validation_embedding)



def preprocess(file_path):
	
	# Read in image from file path
	byte_img = tf.io.read_file(file_path)

	# Load in the image 
	img = tf.io.decode_jpeg(byte_img)
	
	# Preprocessing steps - resizing the image to be 100x100x3
	img = tf.image.resize(img, (100,100))
	# Scale image to be between 0 and 1 
	img = img / 255.0

	# Return image
	return img




class FR_class:

	def __init__(self, model_file):

		self.model = tf.keras.models.load_model(model_file, custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy}, compile=False)



	def verify(self, detection_threshold, verification_threshold, empid):
		results = []
		for image in os.listdir(os.path.join('media', 'verify', empid)):
			input_img = preprocess(os.path.join('media', 'verify', 'verify_test' , 'inputImage.jpg'))
			validation_img = preprocess(os.path.join('media', 'verify', empid, image))
	
			# Make Predictions 
			result = self.model.predict(list(np.expand_dims([input_img, validation_img], axis=1)))
			results.append(result)


		detection = np.sum(np.array(results) > detection_threshold)
		# Verification Threshold: Proportion of positive predictions / total positive samples 
		verification = detection / len(os.listdir(os.path.join('media', 'verify', empid)))
		verified = verification > verification_threshold
		return results, verified

