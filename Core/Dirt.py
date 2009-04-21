import os
import yaml
class Dirt(object):
	def dirtExists(self):
		if os.path.exists("dirt"):
			return True
		else:
			return False
	def loadDirt(self):
		DirtFile = open('dirt', 'r')
		DFile = DirtFile.read()
		G_Yaml = yaml.load(DFile)
		return G_Yaml