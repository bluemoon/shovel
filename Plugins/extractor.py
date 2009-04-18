from Configurator import Configurator
from Debug import Debug
import os
import tarfile

class extractor:
	def __init__(self):
		self.Config = Configurator()
	def run(self):
		Attr = getattr(self,self.Command)
		Attr(self.File)
        
	def tar(self,Name):
		Config = self.Config.GetConfig(Name)
		Debug(Config,"DEBUG")
	 	File= Config["file"]
		print "[tar] Extracting: " + File
		if os.path.exists("tmp/"+File):
			End = File.split(".")
			if End[-1] == "bz2":
				tar = tarfile.open(name="tmp/" + File,mode='r:bz2')
				extract = tar.extractall(path="tmp",members=None)
			if End[-1] == "gz":
				tar = tarfile.open(name="tmp/" + File,mode='r:gz')
				extract = tar.extractall(path="tmp",members=None)