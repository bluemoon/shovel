from Core.Configurator import Configurator
from Core.Debug import Debug
import os
import tarfile

def ExtractNameFromTar(Tar):
	Tar = Tar.split(".")[:-2]
	return ".".join(Tar)

class extractor:
	def __init__(self):
		self.Config = Configurator()

	def tar(self,Name):
		Tar = {}
		Config = self.Config.GetConfig(Name)
		Debug(Config,"DEBUG")
	 	File = Config["file"]
		self.Config.CreateOutYaml(Name)
		if not os.path.exists("tmp/downloads/"+ExtractNameFromTar(File)):
			print "[tar] Extracting: " + File
			if os.path.exists("tmp/downloads/"+File):
				End = File.split(".")
				if End[-1] == "bz2":
					tar = tarfile.open(name="tmp/downloads/" + File,mode='r:bz2')
					extract = tar.extractall(path="tmp/downloads/",members=None)
				if End[-1] == "gz":
					tar = tarfile.open(name="tmp/downloads/" + File,mode='r:gz')
					extract = tar.extractall(path="tmp/downloads/",members=None)