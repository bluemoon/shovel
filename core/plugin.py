#!/usr/bin/env python
##############################################################################
## File: Plugin.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Imports ##########################################################
import os
import sys
import fnmatch

#### Local Imports ###########################################################
from core.loader       import CoreHandler
from core.configurator import Configurator
from core.debug        import *
from core.terminal import TermGreen
from core.terminal import TermEnd

import plugins as Plugins

#### Class:Plugin ############################################################
'''plugins = {
    'shovel':{
        'systools' : {
            'builder':{
                'waf' :['configure','build'],
                'make':['configure','build'],
                
            },
            'downloader':{
                'http': ['download'],
                'svn' : ['checkout',]
            }
        }
        
    }
} '''
class plugin:
    def __init__(self):
        """docstring for __init__"""
        self.splitString = '.'
        
    def load(self, use):
        #reduce(dict.get, use.split(self.splitString), )
class Plugin:
    def __init__(self):
        self.loader = CoreHandler()
        self.config = Configurator()
	
    def loadAll(self, folder=None):
        Dir = os.path.join(os.path.dirname(__file__)).split("/")[:-2]
        def locate(pattern, root=Plugins.__dict__['__path__'][0]):
            for path, dirs, files in os.walk(root):
                for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
                    yield filename

        for Py in locate("*.py",Plugins.__dict__['__path__'][0]):
            self.loadAbsolute(Py)

    def loadAbsolute(self, absPath):
        absSplit = absPath.split('/')
        file = absSplit[-1:]
        nFile = file[0].split(".") 
        module = self.load(nFile[0],"/".join(absSplit[:-1]))
        self.config.putModuleLoaded(nFile[0])

    def load(self, name=None, folder=None):
        self.config.putFeature('shovel.'+name.lower())
        self.loader.Load(name,folder)
        loader = self.loader.GetModule(name)
        try:
            if name != "__init__":
                for Function in loader.__dict__[name].__dict__:
                    if Function[0:2] != '__':
                        self.config.putFeature('shovel.'+name.lower()+"." +Function)
                        debug('Loaded: '+ TermGreen +'shovel.'+name.lower()+"." +Function + TermEnd,INFO)

        except AttributeError:
            pass

