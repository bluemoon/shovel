#!/usr/bin/env python
### System Includes ###
import sys
import os
import yaml
import threading
import imp
import re
import fnmatch
import time
import inspect
from threading import Thread

sys.path.append('Core/')
#### From Core ####
from Messaging  import CoreMessaging
from Terminal import TermGreen,TermOrange,TermEnd
from Configurator import Configurator,feature
from Loader import CoreHandler
from Debug import Debug,SetDebug
from Dependencies import Dependencies

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
#  Requires class instance ->
#  2. Then a function will pass over each class and use __dict__ to determine the functions and will add to the configurator
#
# Any code that has 
#### FROZEN ####
# has been feature frozen and will not be changed


#### FROZEN ####
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
#### END FROZEN ####

class Blocks(object):
	def ParseBlock(self,Yaml,Reverse=False):
		Block = []
		if hasattr(Yaml, 'keys'):
			for Blocks in Yaml.keys():
			 	Block.append(Blocks)
		if Reverse:
			Block.reverse()
		return Block

class Features(object):
	def __init__(self):
		self.Loader = CoreHandler()
		self.Config = Configurator()
	def SplitByClass(self,Search):
		Temp = Search.split(".")
		return ".".join(Temp[:2])
	def SplitClass(self,Search):
		Temp = Search.split(".")
		return Temp[1:2][0]
	def SplitFunction(self,Search):
		Temp = Search.split(".")
		return Temp[-1:][0]
	def RunFeature(self,Feature,Name):
		if hasattr(Feature, 'keys'):
			for Use in Feature.keys():
				if Use == 'use':
					Module = self.Loader.GetModule(self.SplitClass(Feature[Use]))
					if hasattr(Module,self.SplitClass(Feature[Use])):
						self.Config.PutConfig(Name,Feature)
						DynamicClass = getattr(Module,self.SplitClass(Feature[Use]))
						DyC = DynamicClass()
						DynamicFunction = getattr(DynamicClass,self.SplitFunction(Feature[Use]))
						DyF = DynamicFunction(DyC,Name)
						
		else:
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
		self.Loader.Load(Name,Folder)
		Loader = self.Loader.GetModule(Name)
   		try:
			for Function in Loader.__dict__[Name].__dict__:
				if Function[0:2] != '__':
					self.Config.putFeature('shovel.'+Name.lower()+"." +Function)
					Debug('Loaded: '+ TermGreen +'shovel.'+Name.lower()+"." +Function + TermEnd,"INFO")
		except AttributeError:
			pass
		
class ShovelNew(object):
	def __init__(self):
		self.Blocks   = Blocks()
		self.Dirt     = Dirt()
		self.Config   = Configurator()
		self.Features = Features()
		self.Plugins  = Plugins()
		self.Deps     = Dependencies()
		self.Commands = []
		
	def CommandOutOfBlock(self,Block):
		for B in Block:
			self.Commands.append(B)
	
	def addArgV(self):
		global __Debug
		__Debug = ""
		# Im going to go to a class based approach soon
		for ArgV in sys.argv[1:]:
			if ArgV == '-v':
				__Debug = "WARNING"
			if ArgV == '-vv':
				__Debug = "INFO"
			if ArgV == '-vvv':
				__Debug = "DEBUG"
			if ArgV == '--sandbox':
				self.Config.PutGlobal("sandbox",True)
				
	def runArgV(self):
		for ArgV in sys.argv[1:]:
			if ArgV in self.Commands:
				self.runBlock(ArgV)
				self.DependencyRunner(ArgV)

	def checkArgV(self):
		""" Checks to see if any arguments were passed """
		Arg = 0
		for ArgV in sys.argv[1:]:
			Arg += 1
		if Arg == 0:
			return False
		else:
			return True
	
	def WorkRunner(self,Block,Work):
		Debug("block: "+Block + " work: " +Work,"DEBUG")
		for work in self.DirtY[Block][Work]:
			if hasattr(work,'keys'):
				for Keys in work.keys():
					if hasattr(work[Keys],'keys'):
						if work[Keys].has_key('use'):
							if self.Config.getFeature(work[Keys]['use']):
								self.Config.PutPackage(Work,self.DirtY[Block][Work])
								self.Features.RunFeature(work[Keys],Work)
							else:
								Debug("Not loaded: "+Work[Keys]['use'],"ERROR")
			else:
				raise Exception('ParseError')
				
	def DependencyRunner(self,Block):
		for Runner in self.DirtY[Block]:
			if hasattr(self.DirtY[Block][Runner],'keys'):
				raise Exception('ParseError')
			else:
				for List in self.DirtY[Block][Runner]:
					if hasattr(List,'keys'):
						if List.has_key('dependencies'):
							if hasattr(List['dependencies'],'keys'):
								if List['dependencies'].has_key('use'):
									pass
							else:
								for Deps in List['dependencies']:
									Debug("[" +Runner + "] depends on: " + Deps,"INFO")
									self.Deps.DependencyGeneratorAdd(Runner,Deps)
						else:
							self.Deps.DependencyGeneratorAdd(Runner)
					else:
						raise Exception('ParseError')
						
		DepList = self.Deps.DependencyGeneratorRun()
		Rev = []
		for RevDep in DepList[0]:
			Rev.append(RevDep)
			
		while Rev:
			Work = Rev.pop()
			self.WorkRunner(Block,Work)
			
	def runFeatureBlock(self,Block):
		Counter = 0
		for Runner in self.Blocks.ParseBlock(self.DirtY[Block],True):
			Debug(Runner,"DEBUG")
			List = self.DirtY[Block][Runner]
			List.reverse()
			print List.pop()
			for subRunner in self.DirtY[Block][Runner]:
				print subRunner
				for mF in self.Blocks.ParseBlock(subRunner):
					if hasattr(subRunner[mF],'keys'):
						if subRunner[mF].has_key('use'):
							print subRunner[mF]['use']
							Feature = self.Config.getFeature(subRunner[mF]['use'])
							if Feature:
								self.Features.RunFeature(subRunner[mF],subRunner)
					if subRunner.has_key('use'):
						print subRunner['use']

					#Debug(subRunner,"DEBUG")
				
	def runBlock(self,Block):
		for Runner in self.Blocks.ParseBlock(self.DirtY[Block]):
			sub = self.Blocks.ParseBlock(self.DirtY[Block][Runner])
			#sub.reverse()
			for SubRunner in sub:
				if SubRunner == 'use':
					Name = self.Features.SplitClass(self.DirtY[Block][Runner][SubRunner])
					Feature = self.Config.getFeature(self.DirtY[Block][Runner][SubRunner])
					if not Feature:
						Debug("Feature " +TermOrange + self.DirtY[Block][Runner][SubRunner] + TermEnd + " is not available","WARNING")
					else:
						Debug("Instance created: "+ TermGreen + self.DirtY[Block][Runner][SubRunner] + TermEnd,"INFO")
						#self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner],Runner)
				#Debug(self.Blocks.ParseBlock(self.DirtY[Block][Runner][SubRunner]),"DEBUG")	
				for uberSubRunner in self.Blocks.ParseBlock(self.DirtY[Block][Runner][SubRunner]):
					if uberSubRunner == 'use':
						Name = self.Features.SplitClass(self.DirtY[Block][Runner][SubRunner][uberSubRunner])
						Feature = self.Config.getFeature(self.DirtY[Block][Runner][SubRunner]['use'])
						if not Feature:
							Debug("Feature "+ TermOrange+ self.DirtY[Block][Runner][SubRunner][uberSubRunner]+TermEnd + " is not available","WARNING")
						else:
							Debug("Instance created: "+ TermGreen + self.DirtY[Block][Runner][SubRunner][uberSubRunner] + TermEnd,"INFO")
							#self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner],Runner)
					else:
						pass
						
	def displayHelp(self):
		MainBlocks = self.Blocks.ParseBlock(self.DirtY)
		print "These are the commands available: " 
		print " ".join(MainBlocks)
			
	def Main(self):
		self.addArgV()
		SetDebug(_ShovelNew__Debug)
		self.Plugins.LoadAll()
		if self.Dirt.dirtExists():
			self.DirtY = self.Dirt.loadDirt()
			BaseBlock = self.Blocks.ParseBlock(self.DirtY)
			self.CommandOutOfBlock(BaseBlock)
			if self.checkArgV():
				self.runArgV()
			else:
				self.displayHelp()
		

if __name__ == "__main__":
	
	M = ShovelNew()
	M.Main()
