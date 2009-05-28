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

def touch(file):
    tfile = open(file, 'w')
    tfile.close()

def chdir(dir):
    ''' Wrapper for os.chdir so that it emits debugging code '''
    debug("Changing to directory: " + dir, DEBUG)
    os.chdir(dir)

def buildPath(base,*dir):
    tmp = base + "/" + "/".join(dir)
    return tmp.replace("//", "/")


def condChroot(chrootPath):
    if chrootPath is not None:
        saved = { "ruid": os.getuid(), "euid": os.geteuid(), }
        uid.setresuid(0,0,0)
        os.chdir(chrootPath)
        os.chroot(chrootPath)
        uid.setresuid(saved['ruid'], saved['euid'])

def mkdirIfAbsent(*args):
    ''' Create a directory if its not there '''
    for dirName in args:
        debug("ensuring that dir exists: %s" % dirName,DEBUG)
        if not os.path.exists(dirName):
            debug("creating dir: %s" % dirName,DEBUG)
            os.makedirs(dirName)
            
                


def rmDirectoryRecursive(path):
    ''' Recursively remove a directory '''
    for i in os.listdir(path):
        fullPath = path + "/" + i
        if os.path.isdir(fullPath):
            ## Recursively delete
            rmDirectoryRecursive(fullPath)
        

    ## Finally delete the parent
    os.rmdir(path)

