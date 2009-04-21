#### System Imports ####
import os
import subprocess
import re
#### Local Imports ####
from Core.Configurator import Configurator
from Core.Debug import Debug
from Core.Terminal import TermGreen,TermEnd


class builder:
	def __init__(self):
		self.Config = Configurator()
		
	def make(self,Name):
		Debug(Name,"DEBUG")
		# Get all the info from the container class
		Config = self.Config.GetConfig(Name)
		Debug(Config,"DEBUG")
		
		File = Config["folder"]
		Configure = Config["configure"]
		CWD = os.getcwd()
		
		if self.Config.GetGlobal("sandbox"):
			if not os.path.exists("tmp/sandbox"):
				os.mkdir('tmp/sandbox')
			if not os.path.exists("tmp/sandbox/"+Name):
				os.mkdir('tmp/sandbox/'+Name)
			
			NewConfigure = "--prefix="+CWD+"/tmp/sandbox/"+Name + " " + " ".join(Configure)
			Debug(NewConfigure,"DEBUG")
			Configure = NewConfigure
		else:
			Configure = " ".join(Configure)
		
		os.chdir('tmp/downloads/'+File)
		Debug("Configuring...","INFO")
		print "[make] Configuring: " + Name
		
		if Configure:
			print "[make] Configure Options: " + Configure
			p = subprocess.Popen('./configure ' + Configure,shell=True,stdout=None)
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
				#pass
				print read[:-1]
			
		o.wait()
		Debug("Build Return Code: %d" % (o.returncode),"INFO")
		if o.returncode > 0:
			raise Exception('BuildError')
			
		if self.Config.GetGlobal("sandbox"):
			Debug("Sandbox Install","INFO")
			SB = subprocess.Popen('make install',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			SB.wait()
			
		os.chdir(CWD)