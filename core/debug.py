## File: Debug.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)

## Local includes
from core.configurator import configurator
## System includes
import inspect
import os


## Static values for debugging
ERROR   = -1
NONE    = 0
WARNING = 1
INFO    = 2
DEBUG   = 3



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
    
    ## Errors
    elif level == -1:
        return 'ERROR'

def _dPrint(level, string, iOuter):
    ''' an internal method that prints the debug strings '''
    rLevel = _levelToString(level)
    builtString = '%s:[%s-%d]: %s' % (rLevel,
    os.path.basename(iOuter[1][1]),iOuter[1][2],string)
    print builtString
    ## return builtString
    ## we must explicitly delete the frame inspector or it will cause 
    ## unnecessary garbage

    
def debug(string, level=DEBUG):
    ''' the debug method, a printer for debugging with verbosity control'''
    config = configurator()
    ## Get the frames so we know who's calling us from what line
    current = inspect.currentframe(0)
    # print inspect.getframeinfo(current)
    # print inspect.stack(current)
    outer   = inspect.getouterframes(current)
    
    ## get the debug level from our global class
    dLevel = int(config.getGlobal('debug'))
    ## Keep a marker so we dont print the same thing more than once
    hasPrinted = False
    
    if dLevel > NONE:
        if dLevel >= level and not hasPrinted:
            hasPrinted = True
            _dPrint(level, string, outer)

    ## we must explicitly delete the frame inspector or it will cause 
    ## unnecessary garbage
    del current    
    


