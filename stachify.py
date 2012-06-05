"""
Stachify your face
==================
"""

import random
import cv2
import requests
import settings
import face

class CleanCut(object):

	def __init(self, url, coordinates=None,):
		self.url = url
		self.coordinates = coordinates
		self.mustache = cv2.imread(settings.mustaches[random.randomint(0,
			len(settings.mustaches))])

	def load(self, url):
		raw_image = requests.get(url)
		self.image = cv2.imdecode(raw_image, 1)

	def place_stache(self):
		return None



def add_stache(url, mouth_center=None, roll=None, size=None)
    """
    Add Stache
    ==========
    @param url: url of image to add stache to.
    @param coordinates: coordinates of mouth.

    @return: local image file. 
    """
	face = CleanCut(url, coordinates=mouth_center)
	return face.place_stache()