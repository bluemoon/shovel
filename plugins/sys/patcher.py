##############################################################################
## File: patcher.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################
import re
import os
import subprocess

from core.configurator import Configurator
from core.debug import *

def ExtractNameFromTar(Tar):
	Tar = Tar.split(".")[:-2]
	return ".".join(Tar)
	
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
		Folder = self.Config.FindInPackage("extract",Name)
		PatchDir = ExtractNameFromTar(Folder['file'])
		CWD = os.getcwd()
		os.chdir("tmp/downloads/" + PatchDir)
		for File in Config["file"]:
			#IntelliPatcher(Files)
			PatchLevel =  File.split('@')
			pLevel = PatchLevel[1].split(':')[1]
			pFile  = PatchLevel[0]
			Patch = subprocess.Popen('patch -p%d < %s' % (int(pLevel),CWD+"/"+pFile), shell=True, stdout=None, stderr=None)
			Patch.wait()
			if Patch.returncode > 0:
				debug("Patch didn't return 0!",WARNING)
		os.chdir(CWD)
		#Debug(Config["link"],"DEBUG")
	
		
