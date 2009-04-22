#!/usr/bin/env python
##############################################################################
## File: OutputParser.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Imports ##########################################################
from threading import Thread
#### Class:GccParse ##########################################################
class GccParse(Thread):
	"""docstring for GccParse"""
	def __init__(self):
		pass
	def ParseStdOut(self,Object):
		Regex = re.compile('[a-zA-Z0-9/_]*\.c')
		while Object.stdout.readline():
			Read = Object.stdout.readline()
			Match = Regex.findall(read)
			if Match:
				PPrint("Compiling: " + Match[0],"ok",None,"GREEN")
			else:
				PPrint("Out: "+Read[:-1],"!!","BLUE","BLUE")
	def ParseStdErr(self):
		pass
		