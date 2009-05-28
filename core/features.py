#!/usr/bin/env python
##############################################################################
## File: Features.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### Local Includes ##########################################################
from core.loader       import CoreHandler
from core.configurator import Configurator
from core.exceptions   import FeatureError
from core.debug        import *

#### Class:Features ##########################################################
class Features(object):
    def __init__(self):
        self.Loader = CoreHandler()
        self.Config = Configurator()

        ### For searches ###
    def SplitByClass(self, Search):
        Temp = Search.split(".")
        return ".".join(Temp[:2])

    def SplitClass(self, Search):
        Temp = Search.split(".")
        return Temp[1:2][0]

    def SplitFunction(self, Search):
        Temp = Search.split(".")
        return Temp[-1:][0]
        
    ### End Searches ###
    def RunFeature(self, use, name, yaml):
        debug(use, DEBUG)
        debug(name, DEBUG)
        debug(yaml, DEBUG)
        
        Module = self.Loader.GetModule(self.SplitClass(use))
        if hasattr(Module, self.SplitClass(use)):
            self.Config.PutConfig(name, yaml)
            debug('class: ' + self.SplitClass(use), DEBUG)
            DynamicClass = getattr(Module, self.SplitClass(use))
            DyC = DynamicClass()
            debug('function: ' + self.SplitFunction(use), DEBUG)
            DynamicFunction = getattr(DynamicClass, self.SplitFunction(use))
            DyF = DynamicFunction(DyC, name)

        
