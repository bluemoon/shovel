#!/usr/bin/env python
##############################################################################
## File: Plugin.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Imports ##########################################################
import os
import sys
import fnmatch

#### Local Imports ###########################################################
from Core.Loader       import CoreHandler
from Core.Configurator import Configurator
from Core.Debug        import Debug
from Core.Terminal     import TermGreen,TermOrange,TermEnd

import Plugins

#### Class:Plugin ############################################################
class Plugin:
	def __init__(self):
		self.Loader = CoreHandler()
		self.Config = Configurator()
				
	def LoadAll(self,Folder=None):
		Dir = os.path.join(os.path.dirname(__file__)).split("/")[:-2]
		def locate(pattern, root=Plugins.__dict__['__path__'][0]):
			for path, dirs, files in os.walk(root):
				for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
					yield filename
					
		for Py in locate("*.py",Plugins.__dict__['__path__'][0]):
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
			if Name != "__init__":
				for Function in Loader.__dict__[Name].__dict__:
					if Function[0:2] != '__':
						self.Config.putFeature('shovel.'+Name.lower()+"." +Function)
						Debug('Loaded: '+ TermGreen +'shovel.'+Name.lower()+"." +Function + TermEnd,"INFO")
		except AttributeError:
			pass

