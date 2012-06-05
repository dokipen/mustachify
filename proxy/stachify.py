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

	def __init__(self, url, coordinates=None, mouth_size=None):
		self.url = url
		self.coordinates = coordinates
		self.mouth_size = mouth_size
		p = PIL.ImageFile.Parser()
		raw = open('mustaches/old-smokey.png').read()
		p.feed(raw)
		self.mustache = p.close()

	def load(self):
		raw_image = requests.get(self.url)
		p = PIL.ImageFile.Parser()
		p.feed(raw_image.content)
		self.image = p.close()

	def place_stache(self):
		transform_matrix = [[1,.5], [.5,1], [1,1]]
		self.load()
		#self.mustache = self.mustache.resize(self.image.size)
		#self.mustache = self.mustache.transform(self.image.size, (1,1,self.coordinates[0], 1, 1, self.coordinates[1]))
		ratio = 1.0 / (self.mustache.size[0] / float(self.mouth_size))
		self.mustache = self.mustache.resize((self.mouth_size, int(self.mustache.size[1] * ratio)))
		tl = (self.coordinates[0] - self.mustache.size[0] / 2,
			  self.coordinates[1] - self.mustache.size[1] / 2)
		self.image.paste(self.mustache, tl, self.mustache)
		print self.mustache.format, self.image.mode, self.mustache.size
		print self.image.format, self.image.mode, self.image.size
		#stache_face = PIL.ImageChops.add(self.image, self.mustache, .5, 0)
		stacheout = 'static/{}.jpg'.format(abs(hash(self.url)))
		#stache_face.save(self.image)
		self.image.save(stacheout)
		return abs(hash(self.url))

def add_stache(url, mouth_center=None, roll=None, size=None):
    """
    Add Stache
    ==========
    @param url: url of image to add stache to.
    @param coordinates: coordinates of mouth.

    @return: local image file. 
    """
    
    face = CleanCut(url, coordinates=mouth_center, mouth_size=size)
    return face.place_stache()
