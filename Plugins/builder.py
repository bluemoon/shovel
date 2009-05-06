##############################################################################
## File: builder.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Imports ##########################################################
import os
import subprocess
import re
#### Local Imports ###########################################################
from Core.Configurator import Configurator
from Core.Debug        import Debug
from Core.Terminal     import TermGreen,TermEnd
from Core.Utils	       import PPrint


class builder:
	def __init__(self):
		self.Config = Configurator()
		
	def make(self,Name):
		Debug(Name,"DEBUG")
		# Get all the info from the container class
		Config = self.Config.GetConfig(Name)
		Debug(Config,"DEBUG")
		
		# Get the function parameters from the container class
		File = Config["folder"]
		Configure = Config["configure"]
		
		# Our working directory
		CWD = os.getcwd()
		# if --sandbox is passed to the main code
		if self.Config.GetGlobal("sandbox"):
			# I dont like the values hardcoded
			if not os.path.exists("tmp/sandbox"):
				os.mkdir('tmp/sandbox')
			os.mkdir('tmp/sandbox/tmp')
			#p = subprocess.Popen('cp tmp/%s tmp/sandbox/tmp/' % (File),shell=True,stdout=None)
			#p.wait()
			
			# This adds --prefix= so that it doesnt install it to the system
			NewConfigure = "--prefix="+ CWD + " " + " ".join(Configure)
			# Prints out the whole string
			Debug(NewConfigure,"DEBUG")
			Configure = NewConfigure
		else:
			# The values should be listified so join them
			Configure = " ".join(Configure)
		
		os.chdir(CWD + '/tmp/downloads/' + File)
		Debug("Configuring...","INFO")
		print "[make] Configuring: " + Name
		
		if Configure:
			print "[make] Configure Options: " + Configure
			p = subprocess.Popen('./configure ' + Configure,shell=True,stdout=None)
			p.wait()
		else:
			p = subprocess.Popen('./configure',shell=True,stdout=None)
			p.wait()
		
		Debug("Building:" + Name,"INFO")
		print "[make] Building: " + Name
		
		regex = re.compile('[a-zA-Z0-9/_]*\.c')
		#warning = re.compile('[a-zA-Z0-9/_]*\.c:[0-9]*:\swarning:[a-zA-Z0-9/_]*')
		if self.Config.GetGlobal("nonpretty"):
			MakeSub = subprocess.Popen('make',shell=True,stdout=None,stderr=None)
			#while MakeSub.poll() is None:
				#Read = MakeSub.stdout.readline()
				#print Read[:-1]
		else:
			MakeSub = subprocess.Popen('make',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			while MakeSub.poll() is None:
				Read = MakeSub.stdout.readline()
				match = regex.findall(Read)
				if match:
					PPrint("Compiling: " + match[0],"ok",None,"GREEN")
				else:
					PPrint("Out: "+Read[:-1],"!!","BLUE","BLUE")
		MakeSub.wait()
		# Make sure the build returns a valid code and doesnt fail
		Debug("Build Return Code: %d" % (MakeSub.returncode),"INFO")
		if MakeSub.returncode > 0:
			raise Exception('BuildError')
		
		if self.Config.GetGlobal("sandbox"):
			Debug("Sandbox Install","INFO")
			SB = subprocess.Popen('make install',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			SB.wait()

		if self.Config.GetGlobal("sandbox"):
			os._exit(0)
		#os.chdir(CWD)
