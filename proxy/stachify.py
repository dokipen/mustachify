"""
Stachify your face
==================
"""

import random
import PIL.ImageFile
import PIL.ImageChops
import requests
import settings
import face

class CleanCut(object):

	def __init__(self, url, coordinates=None,):
		self.url = url
		self.coordinates = coordinates
		p = PIL.ImageFile.Parser()
		raw = open('mustaches/handlebar.jpg').read()
		p.feed(raw)
		self.mustache = p.close()

	def load(self):
		raw_image = requests.get(self.url)
		p = PIL.ImageFile.Parser()
		p.feed(raw_image.content)
		self.image = p.close()

	def place_stache(self):
		transform_matrix = [[0,0], [1,1], [2,2]]
		self.load()
		self.mustache = self.mustache.resize(self.image.size)
		stache_face = PIL.ImageChops.add(self.image, self.mustache, 1, 50)

		stacheout = '{}.jpg'.format(abs(hash(self.url)))
		stache_face.save(stacheout)
		return stacheout

def add_stache(url, mouth_center=None, roll=None, size=None):
    """
    Add Stache
    ==========
    @param url: url of image to add stache to.
    @param coordinates: coordinates of mouth.

    @return: local image file. 
    """
    
    face = CleanCut(url, coordinates=mouth_center)
    return face.place_stache()
