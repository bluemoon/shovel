import os
import subprocess

from Core.Configurator import Configurator
from Core.Debug import *

class systools:
	def __init__(self):
		pass
	def pkgconfig(self,Name):
		p = subprocess.Popen("/usr/bin/env pkg-config",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		while p.stdout.readline():
			if p.stdout.readline() != "Must specify package names on the command line":
				debug("pkg-config not found!",ERROR)
			else:
				debug("pkg-config found!",INFO)
