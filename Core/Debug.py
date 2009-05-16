## File: Debug.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)

## Local includes
from Core.Configurator import Configurator

## System includes
import inspect
import os

## Static values for debugging
NONE    = 0
WARNING = 1
INFO    = 2
DEBUG   = 3
ERROR   = 4


def _levelToString(level):
    ''' an internal method that converts the numerical value to
        a usable string. '''
        
    if level == 0:
        return 'NONE'
    elif level == 1:
        return 'WARNING'
    elif level == 2:
        return 'INFO'
    elif level == 3:
        return 'DEBUG'

def _dPrint(level, string, iOuter):
    ''' an internal method that prints the debug strings '''
    rLevel = _levelToString(level)
    print '%s:[%s-%d]: %s' % (rLevel,
    os.path.basename(iOuter[1][1]),iOuter[1][2],string)
    ## we must explicitly delete the frame inspector or it will cause 
    ## unnecessary garbage
    del iOuter
    
def debug(string, level=DEBUG):
    ''' the debug method, a printer for debugging with verbosity control'''
    config = Configurator()
    ## Get the frames so we know who's calling us from what line
    current = inspect.currentframe()
    outer   = inspect.getouterframes(current)
    
    ## get the debug level from our global class
    dLevel = int(config.GetGlobal('debug'))
    ## Keep a marker so we dont print the same thing more than once
    hasPrinted = False
    
    if dLevel > NONE:
        if dLevel >= level and not hasPrinted:
            hasPrinted = True
            _dPrint(level,string,outer)

        
    


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
