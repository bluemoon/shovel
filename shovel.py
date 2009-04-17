### System Includes ###
import sys
import os
import yaml
import threading
import imp
import re
import fnmatch
from threading import Thread

sys.path.append('Core')
#### From ModularCore ####
sys.path.append('Plugins/PackageBuilder')
from PackageBuilder import PackageBuilder
#### From Core ####
from Messaging  import CoreMessaging
from Terminal import TermGreen,TermEnd
from Configurator import Configurator,feature
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
# 
# Plugins:
# [x] 1. So the plugin loader will recurse the directory and load all of the plugins.
#  2. Then a function will pass over each class and use __dict__ to determine the functions and will add to the configurator


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
		Block = []
		if hasattr(Yaml, 'keys'):
			for Blocks in Yaml.keys():
			 	Block.append(Blocks)
			
		return Block

class Features(object):
	def SplitByClass(self,Search):
		Temp = Search.split(".")
		return ".".join(Temp[:2])
	def RunFeature(self,Feature):
		pass
class Plugins:
	def __init__(self):
		self.Loader = CoreHandler()
		self.Config = Configurator()
				
	def LoadAll(self,Folder=None):
		def locate(pattern, root=os.getcwd()):
			for path, dirs, files in os.walk(root):
				for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
					yield filename
		for Py in locate("*.py","Plugins"):
			self.LoadAbsolute(Py)
	def LoadAbsolute(self,AbsPath):
		AbsSplit = AbsPath.split('/')
		File = AbsSplit[-1:]
		nFile = File[0].split(".") 
		Module = self.Load(nFile[0],"/".join(AbsSplit[:-1]))
		self.Config.putModuleLoaded(nFile[0])
	def Load(self,Name=None,Folder=None):
		self.Config.putFeature('shovel.'+Name.lower())
		return self.Loader.Load(Name,Folder)

class ShovelNew(object):
	def __init__(self):
		self.Blocks = Blocks()
		self.Dirt = Dirt()
		self.Config = Configurator()
		self.Features = Features()
		self.Plugins = Plugins()
		self.Commands = []
	def CommandOutOfBlock(self,Block):
		for B in Block:
			self.Commands.append(B)
	
	def runArgV(self):
		for ArgV in sys.argv[1:]:
			if ArgV in self.Commands:
				self.runBlock(ArgV)
	def checkArgV(self):
		Arg = 0
		for ArgV in sys.argv[1:]:
			Arg += 1
		if Arg == 0:
			return False
		else:
			return True
	def runBlock(self,Block):
		for Runner in self.Blocks.ParseBlock(self.DirtY[Block]):
			for SubRunner in self.Blocks.ParseBlock(self.DirtY[Block][Runner]):
				if SubRunner == 'use':
					Search = self.Features.SplitByClass(self.DirtY[Block][Runner][SubRunner])
					Feature = self.Config.getFeature(Search)
					if not Feature:
						print "The feature " + self.DirtY[Block][Runner][SubRunner] + " is not available"
					else:
						print "Is loaded: "+ TermGreen + self.DirtY[Block][Runner][SubRunner] + TermEnd
						self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner])
						
				for uberSubRunner in self.Blocks.ParseBlock(self.DirtY[Block][Runner][SubRunner]):
					if uberSubRunner == 'use':
						Search = self.Features.SplitByClass(self.DirtY[Block][Runner][SubRunner][uberSubRunner])
						Feature = self.Config.getFeature(Search)
						if not Feature:
							print "The feature " + self.DirtY[Block][Runner][SubRunner][uberSubRunner] + " is not available"
						else:
							print "Is loaded: "+ TermGreen + self.DirtY[Block][Runner][SubRunner][uberSubRunner] + TermEnd
							self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner])
					else:
						pass
						
	def displayHelp(self):
		print self.Blocks.ParseBlock(self.DirtY)
			
	def Main(self):
		self.Plugins.LoadAll()
		if self.Dirt.dirtExists():
			self.DirtY = self.Dirt.loadDirt()
			BaseBlock = self.Blocks.ParseBlock(self.DirtY)
			self.CommandOutOfBlock(BaseBlock)
			if self.checkArgV():
				self.runArgV()
			else:
				self.displayHelp()
		
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
    M = ShovelNew()
    M.Main()
