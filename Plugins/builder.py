from Configurator import Configurator
from Debug import Debug
from Terminal import TermGreen,TermEnd

import os
import subprocess
import re

class builder:
	def __init__(self):
		self.Config = Configurator()
	def run(self):
		Attr = getattr(self,self.Command)
		Attr(self.Filename)
	def make(self,Name):
		Debug(Name,"DEBUG")
		Config = self.Config.GetConfig(Name)
		Debug(Config,"DEBUG")
		File = Config["folder"]
		Configure = Config["configure"]
		CWD = os.getcwd()
			
		os.chdir('tmp/'+File)
		Debug("Configuring...","INFO")
		print "[make] Configuring: " + Name
		
		if Configure:
			print "[make] Configure Options: " + " ".join(Configure)
			p = subprocess.Popen('./configure ' + " ".join(Configure),shell=True,stdout=subprocess.PIPE)
			while p.stdout.readline():
				pass
			p.wait()
		else:
			p = subprocess.Popen('./configure',shell=True,stdout=subprocess.PIPE)
			while p.stdout.readline():
				pass
			p.wait()
		
		Debug("Building:" + Name,"INFO")
		print "[make] Building: " + Name
		
		o = subprocess.Popen('make',shell=True,stdout=subprocess.PIPE,stderr=None)
		regex = re.compile('[a-zA-Z0-9/_]*\.c')
		warning = re.compile('[a-zA-Z0-9/_]*\.c:[0-9]*:\swarning:[a-zA-Z0-9/_]*')
		while o.stdout.readline():
			read = o.stdout.readline()
			match = regex.findall(read)
			if match:
				print "Compiling: " + match[0] + "      [" +TermGreen + "ok" + TermEnd +"]"
			else:
				print read[:-1]
			
		o.wait()
		os.chdir(CWD)