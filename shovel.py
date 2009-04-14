### System Includes ###
import sys
import os
import yaml
import threading
import imp
from threading import Thread

sys.path.append('Core')
#### From ModularCore ####
sys.path.append('Modules/PackageBuilder')
from PackageBuilder import PackageBuilder
#### From Core ####
from Messaging  import CoreMessaging

### For the term coloring ###
TermGreen = "\033[1;32m"
TermEnd   = "\033[1;m"

class Shovel:
	"""docstring for Shovel"""
	def __init__(self, arg=None):
		self.arg = arg
		
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
		
	def getDirtModules(self,Yaml):
		Modules = []
		for List in Yaml:
			for Package in List:
				if Package not in Modules:
					Modules.append(Package)
		if Modules:
			return Modules
		else:
			return False
	
	def loadDirtModules(self,Modules):
		for Mod in Modules:
			#sys.path.append('Modules')
			#print Mod
			self.loadDirtModClass(Mod,Mod)
			
	def loadDirtModClass(self,Module,Name):
		Class = getattr(sys.modules[Module],Name)
		print Class.__dict__
		A = Class()
		A.Main()
				
	def Main(self):
		if self.dirtExists():
			self.Yaml = self.loadDirt()
			self.Modules = self.getDirtModules(self.Yaml)
			self.loadDirtModules(self.Modules)
		
if __name__ == "__main__":
    M = Shovel()
    M.Main()
