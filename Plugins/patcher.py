import re
import os

from Core.Configurator import Configurator
from Core.Debug import Debug,GetDebug

def locate(pattern, root=os.getcwd()):
	for path, dirs, files in os.walk(root):
		for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
			yield filename
			
def IntelliPatcher(PatchFile):
	Pmatch = re.compile('(\+|\-){3}\s[a-zA-Z0-9_/\.-]*')
	FileM = re.compile('[a-zA-Z0-9_/\.-]*')
	File = open(PatchFile,"r")
	while File.readline():
		Line = File.readline()
		G = Pmatch.match(Line)
		if G:
			print G.group()
	for C in locate("*.c","tmp"):
		print C
			

class patcher(object):
	def __init__(self):
		self.Config = Configurator()
	def patch(self,Name):
		Config = self.Config.GetConfig(Name)
		self.Config.CreateOutYaml(Name)
		for Files in Config["file"]:
			#IntelliPatcher(Files)
			print Files.split('@')
		#Debug(Config["link"],"DEBUG")
	
		