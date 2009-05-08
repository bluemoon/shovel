#!/usr/bin/env python
##############################################################################
## File: Debug.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Includes #########################################################
import inspect
import os

NONE    = 0
WARNING = 1
INFO    = 2
DEBUG   = 3

global __Debug
global _ShovelNew__Debug

__Debug = "INFO"
_ShovelNew__Debug = "NONE"
def SetDebug(Level):
	global _ShovelNew__Debug
	_ShovelNew__Debug = Level
def GetDebug():
	return _ShovelNew__Debug
def GreaterThan(Level):
	if Level == "INFO":
		pass
def Debug(Print,Level="DEBUG"):
	Current = inspect.currentframe()
	Outer   = inspect.getouterframes(Current)
	if __Debug != "NONE" or _ShovelNew__Debug:
		if _ShovelNew__Debug == "DEBUG":
			print '%s:[%s-%d]: %s' % (Level,os.path.basename(Outer[1][1]),Outer[1][2],Print)
		if _ShovelNew__Debug == "INFO":
			if Level == "WARNING" or Level == "INFO" or Level == "ERROR":
				print '%s:[%s-%d]: %s' % (Level,os.path.basename(Outer[1][1]),Outer[1][2],Print)
		if _ShovelNew__Debug == "WARNING":		
			if Level == _ShovelNew__Debug or Level == "ERROR":
				print '%s:[%s-%d]: %s' % (Level,os.path.basename(Outer[1][1]),Outer[1][2],Print)
