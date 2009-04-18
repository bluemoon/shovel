import os
import subprocess

from Configurator import Configurator
from Debug import Debug,GetDebug

class systools:
	def __init__(self):
		pass
	def pkgconfig(self,Name):
		p = subprocess.Popen("/usr/bin/env pkg-config",shell=True,stdout=subprocess.PIPE)
		while p.stdout.readline():
			if p.stdout.readline() != "Must specify package names on the command line":
				Debug("pkg-config not found!","ERROR")
			else:
				Debug("pkg-config found!","INFO")