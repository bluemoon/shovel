import os
import sys
import fnmatch

from Core.Loader       import CoreHandler
from Core.Configurator import Configurator
from Core.Debug        import Debug
from Core.Terminal     import TermGreen,TermOrange,TermEnd


import Plugins

class Plugin:
	def __init__(self):
		self.Loader = CoreHandler()
		self.Config = Configurator()
				
	def LoadAll(self,Folder=None):
		Dir = os.path.join(os.path.dirname(__file__)).split("/")[:-2]
		#Debug(Plugins.__dict__['__path__'][0],"DEBUG")
		def locate(pattern, root=Plugins.__dict__['__path__'][0]):
			for path, dirs, files in os.walk(root):
				for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
					yield filename
					
		for Py in locate("*.py",Plugins.__dict__['__path__'][0]):
			#Debug(Py,"DEBUG")
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
