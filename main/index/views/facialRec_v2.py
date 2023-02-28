import cv2
import os
import random
import numpy as np
import math





class FR_v2_class:

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

