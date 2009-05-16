#!/usr/bin/env python
''' File utility module '''
## File: File.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)

## System Includes
import os
## Local Includes
from Core.Debug import *

def mkdirIfAbsent(*args):
    ''' Create a directory if its not there '''
    for dirName in args:
        debug("ensuring that dir exists: %s" % dirName,DEBUG)
        if not os.path.exists(dirName):
            try:
                debug("creating dir: %s" % dirName,DEBUG)
                os.makedirs(dirName)
            except OSError, error:
                print "Could not create dir %s. Error: %s" % (dirName, error)


def rmDirectoryRecursive(path):
    ''' Recursively remove a directory '''
    for i in os.listdir(path):
        fullPath = path + "/" + i
        if os.path.isdir(fullPath):
            ## Recursively delete
            rmDirectoryRecursive(fullPath)
        else:
            os.remove(fullPath)

    ## Finally delete the parent
    os.rmdir(path)

