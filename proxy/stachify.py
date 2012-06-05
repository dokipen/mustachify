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

	def __init__(self, url):
		self.url = url
		p = PIL.ImageFile.Parser()
		raw = open('mustaches/old-smokey.png').read()
		p.feed(raw)
		self.mustache = p.close()
		self.load()

	def load(self):
		raw_image = requests.get(self.url)
		p = PIL.ImageFile.Parser()
		p.feed(raw_image.content)
		self.image = p.close()

	def place_stache(self, face):
		ratio = 1.0 / (self.mustache.size[0] / float(face['size']))
		mustache = self.mustache.resize((face['size'], int(self.mustache.size[1] * ratio)))
		tl = (face['mouth_center'][0] - mustache.size[0] / 2,
			  face['mouth_center'][1] - mustache.size[1] / 2)
		self.image.paste(mustache, tl, mustache)

	def save(self):
		stacheout = 'static/{}.jpg'.format(abs(hash(self.url)))
		#stache_face.save(self.image)
		self.image.save(stacheout)
		return abs(hash(self.url))


def add_stache(url, faces):#mouth_center=None, roll=None, size=None):
    """
    Add Stache
    ==========
    @param url: url of image to add stache to.
    @param coordinates: coordinates of mouth.

    @return: local image file. 
    """
    
    im = CleanCut(url)
    for face in faces:
    	im.place_stache(face) 
    return im.save()
