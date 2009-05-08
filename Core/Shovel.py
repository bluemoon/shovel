##############################################################################
## File: Shovel.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/05/08
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################
#### System Includes #########################################################
from threading import Thread
import sys
import os
import yaml
import threading
import imp
import re
import fnmatch
import time
import inspect

sys.path.append('Core/')
#### From Core ###############################################################
from Core.Messaging     import CoreMessaging
from Core.Terminal      import TermGreen,TermOrange,TermBlue,TermEnd
from Core.Configurator  import Configurator,feature
from Core.Loader        import CoreHandler
from Core.Debug         import Debug,SetDebug
from Core.Dependencies  import Dependencies
from Core.Blocks        import Blocks
from Core.Dirt          import Dirt
from Core.Features      import Features
from Core.Plugin        import Plugin
from Core.File			import rmDirectoryRecursive
from Core.Utils			import PPrint


#from Core.Lexer import Lexi

import Plugins

# Attempt to speed this up a little
try:
    import psyco
    psyco.full()
except ImportError:
    Debug("Psyco not loaded.","INFO")
else:
	Debug("Psyco Enabled!","INFO")


#
# Any code that has 
#### FROZEN ####
# has been feature frozen and will not be changed

def StringParse(self,String):
    Parse = re.compile("\{[a-zA-Z]*\:[a-zA-Z0-9]*\}")
    ParseGroup = Parse.group()
    print ParseGroup
    
#### Class:ShovelNew #########################################################
class ShovelNew(object):
	def __init__(self):
		self.Blocks   = Blocks()
		self.Dirt     = Dirt()
		self.Config   = Configurator()
		self.Features = Features()
		self.Plugins  = Plugin()
		self.Deps     = Dependencies()
		self.Commands = []
                self.OS = os.uname()
                
        def BlockOSspecific(self,Block):
            for OS in Block:
                if OS == self.OS[0]:
                    return True

            
	def CommandOutOfBlock(self,Block):
		for B in Block:
			self.Commands.append(B)
		
	def addArgV(self):
		global __Debug
		__Debug = ""
		ArgCounter = 0
		# Im going to go to a class based approach soon
		for ArgV in sys.argv[1:]:
			if ArgV == '-v':
				__Debug = "WARNING"
				ArgCounter += 1
			if ArgV == '-vv':
				__Debug = "INFO"
				ArgCounter += 1
			if ArgV == '-vvv':
				__Debug = "DEBUG"
				ArgCounter += 1
			if ArgV == '--sandbox':
				ArgCounter += 1
				self.Config.PutGlobal("sandbox",True)
			if ArgV == '--np':
				ArgCounter += 1
				self.Config.PutGlobal("nonpretty",True)
			if ArgV == '--clean':
				ArgCounter += 1
				print "Cleaning up."
				rmDirectoryRecursive("tmp/")
				sys.exit(0)	
				
		if ArgCounter == self.checkArgV():
			print "No options passed assuming",
			print " [" + TermBlue + "all"+ TermEnd + "]"
			self.RunAll = True
		else:
			self.RunAll = False
			
	def runArgV(self):
		if self.RunAll == True:
			for All in self.Commands:
				self.runBlock(All)
				self.DependencyRunner(All)
		else:
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
			return Arg
	
	def WorkRunner(self,Block,Work):
		Debug("block: "+Block + " work: " +Work,"DEBUG")
		for work in self.DirtY[self.OS[0]][Block][Work]:
			if hasattr(work,'keys'):
				for Keys in work.keys():
					if hasattr(work[Keys],'keys'):
						if work[Keys].has_key('use'):
							if self.Config.getFeature(work[Keys]['use']):
								self.Config.PutPackage(Work,self.DirtY[self.OS[0]][Block][Work])
                                                                print Work
								self.Features.RunFeature(work[Keys],Work)
							else:
								Debug("Not loaded: "+Work[Keys]['use'],"ERROR")
			else:
				raise Exception('ParseError')
				
	def DependencyRunner(self,Block):
		for Runner in self.DirtY[self.OS[0]][Block]:
			if hasattr(self.DirtY[self.OS[0]][Block][Runner],'keys'):
				raise Exception('ParseError')
			else:
				for List in self.DirtY[self.OS[0]][Block][Runner]:
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
            for Runner in self.Blocks.ParseBlock(self.DirtY[self.OS[0]][Block]):
			sub = self.Blocks.ParseBlock(self.DirtY[self.OS[0]][Block][Runner])
			#sub.reverse()
			for SubRunner in sub:
				if SubRunner == 'use':
					Name = self.Features.SplitClass(self.DirtY[self.OS[0]][Block][Runner][SubRunner])
					Feature = self.Config.getFeature(self.DirtY[self.OS[0]][Block][Runner][SubRunner])
					if not Feature:
						Debug("Feature " +TermOrange + self.DirtY[Block][Runner][SubRunner] + TermEnd + " is not available","WARNING")
					else:
						Debug("Instance created: "+ TermGreen + self.DirtY[Block][Runner][SubRunner] + TermEnd,"INFO")
						#self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner],Runner)
				#Debug(self.Blocks.ParseBlock(self.DirtY[Block][Runner][SubRunner]),"DEBUG")	
				for uberSubRunner in self.Blocks.ParseBlock(self.DirtY[self.OS[0]][Block][Runner][SubRunner]):
					if uberSubRunner == 'use':
						Name = self.Features.SplitClass(self.DirtY[self.OS[0]][Block][Runner][SubRunner][uberSubRunner])
						Feature = self.Config.getFeature(self.DirtY[self.OS[0]][Block][Runner][SubRunner]['use'])
						if not Feature:
							Debug("Feature "+ TermOrange+ self.DirtY[self.OS[0]][Block][Runner][SubRunner][uberSubRunner]+TermEnd + " is not available","WARNING")
						else:
							Debug("Instance created: "+ TermGreen + self.DirtY[self.OS[0]][Block][Runner][SubRunner][uberSubRunner] + TermEnd,"INFO")
							#self.Features.RunFeature(self.DirtY[Block][Runner][SubRunner],Runner)
					else:
						pass
						
	def displayHelp(self):
		MainBlocks = self.Blocks.ParseBlock(self.DirtY)
		print "These are the commands available: " 
		print " ".join(MainBlocks)
        
	def Main(self):
		self.addArgV()
		#PPrint("Testing prettyPrint",'ok',None,'GREEN')
                #lexi = Lexi()
                #lexi.loadLexer("dirt")
                #lexi.runLexer()
		SetDebug(_ShovelNew__Debug)
		self.Plugins.LoadAll()
		if self.Dirt.dirtExists():
			self.DirtY = self.Dirt.loadDirt()
                        OsBlock = self.Blocks.ParseBlock(self.DirtY)
                        OsSpecific = self.BlockOSspecific(OsBlock)
                        #print OsSpecific
                        if OsSpecific:
                            BaseBlock = self.Blocks.ParseBlock(self.DirtY[self.OS[0]])
                            self.CommandOutOfBlock(BaseBlock)
			self.checkArgV()
			self.runArgV()
			
		
