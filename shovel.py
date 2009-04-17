### System Includes ###
import sys
import os
import yaml
import threading
import imp
import re
from threading import Thread

sys.path.append('Core')
#### From ModularCore ####
sys.path.append('Plugins/PackageBuilder')
from PackageBuilder import PackageBuilder
#### From Core ####
from Messaging  import CoreMessaging
from Terminal import TermGreen,TermEnd
from Configurator import Configurator
from Loader import CoreHandler

# Data Model:
#  {"package": 
#             {"features" : {"x.y.z","z.y.x"},
#			    "module" : {"instance": ""}
# 			}
# }
#  Feature list with sorted dependencies
#  Config for each package linked to its feature list
#  Module list linked with the package
#  Instance list linked with the package
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
class Blocks(object):
	def ParseBlock(self,Yaml,X=None):
		print Yaml
		if X:
			if hasattr(Yaml, 'keys'):
				print X
				for Blocks in Yaml.keys()[X]:
					X = Blocks
					self.ParseBlock(Yaml.keys(),X)
		else:
			for Blocks in Yaml.keys():
				X = Blocks
				self.ParseBlock(Yaml.keys(),X)
				

class FuckYou(object):
	def __init__(self):
		self.Blocks = Blocks()
		self.Dirt = Dirt()
	def Main(self):
		if self.Dirt.dirtExists():
			Dirt = self.Dirt.loadDirt()
			self.Blocks.ParseBlock(Dirt)
		
		
class Shovel:
	"""docstring for Shovel"""
	def __init__(self, arg=None):
		self.arg = arg
		self.Configure = Configurator()
		self.Loader = CoreHandler()
		
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
	
	def extractModuleYaml(self,Yaml,Module):
		ModuleYaml = []
		for List in Yaml:
			for Package in List:
				if Module in List:
					ModuleYaml.append(List[Module])
		
		if not ModuleYaml:
			return False
		else:
			return ModuleYaml
				
	def getDirtModules(self,Yaml):
		Modules = []
		for List in Yaml:
			if List not in Modules:
				Modules.append(List)
		if Modules:
			return Modules
		else:
			return False
	def getDirtSubModule(self,Yaml,Module):
		Md = {}
		for Mod in Yaml[Module]:
			Md[Mod] = Yaml[Module][Mod]
		if Md:
			return Md
		else:
			return False
	
	def loadDirtModules(self,Modules):
		for Mod in Modules:
			#sys.path.append('Modules')
			#print Mod
			self.loadDirtModClass(Mod,Mod)
		
	def loadDirtModClass(self,Module,Name):
		Class = getattr(sys.modules[Module],Name)
		#print Class.__dict__
		A = Class()
		Yaml = self.extractModuleYaml(self.Yaml,Module)
		A.NewMain(Yaml)
	def parseUseFlags(self,Key):
		return Key.split('.')
	def checkKeyList(self,Key):
		return True
	def createModuleInstance(self,Module):
		return Module
	def KeyChecker(self,Yaml):
		for Keys in Yaml.keys():
			if Keys == 'use':
				if self.checkKeyList(Yaml[Keys]):
					Module = self.Loader.Load(self.parseUseFlags(Yaml[Keys])[1],"Plugins")
					self.createModuleInstance(Yaml[Keys])
			else:
				if hasattr(Yaml[Keys], 'keys'):
					for SubKeys in Yaml[Keys].keys():
						if SubKeys == 'use':
							if self.checkKeyList(Yaml[Keys][SubKeys]):
								Module = self.Loader.Load(self.parseUseFlags(Yaml[Keys][SubKeys])[1],"Plugins")
								Instance = self.createModuleInstance(Yaml[Keys][SubKeys])
		
	def Main(self):
		self.Runner = {}
		if self.dirtExists():
			self.Yaml = self.loadDirt()
			self.Modules = self.getDirtModules(self.Yaml)
			for Module in self.Modules:
				for Arg in sys.argv[1:]:
					if Module == Arg:
						self.Runner[Arg] = self.getDirtSubModule(self.Yaml,Module)
						for I in self.getDirtModules(self.Runner[Arg]):
							self.Configure.PutConfig(Arg,self.Runner[Arg])
							self.KeyChecker(self.getDirtSubModule(self.Runner[Arg],I))
							print I
						
			#print self.Configure.GetConfig("ffmpeg")
			#self.loadDirtModules(self.Modules)
		
if __name__ == "__main__":
    M = Shovel()
    M.Main()
