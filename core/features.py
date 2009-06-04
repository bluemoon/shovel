## File: Features.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


#### Local Includes ##########################################################
from core.loader       import coreHandler
from core.configurator import configurator
from core.exceptions   import FeatureError
from core.debug        import *

class features(object):
    def __init__(self):
        self.Loader = CoreHandler()
        self.Config = configurator()

        ### For searches ###
    def splitByClass(self, Search):
        Temp = Search.split(".")
        return ".".join(Temp[:2])

    def splitClass(self, Search):
        Temp = Search.split(".")
        return Temp[1:2][0]

    def splitFunction(self, Search):
        Temp = Search.split(".")
        return Temp[-1:][0]
        
    ### End Searches ###
    #def RunFeature(self, use, name, yaml):
    #    debug(use,  DEBUG)
    #    debug(name, DEBUG)
    #    debug(yaml, DEBUG)
    #    
    #    Module = self.Loader.GetModule(self.splitClass(use))
    #    if hasattr(Module, self.splitClass(use)):
    #        self.Config.putConfig(name, yaml)
    #        debug('class: ' + self.splitClass(use), DEBUG)
    #        DynamicClass = getattr(Module, self.splitClass(use))
    #        DyC = DynamicClass()
    #        debug('function: ' + self.splitFunction(use), DEBUG)
    #        DynamicFunction = getattr(DynamicClass, self.splitFunction(use))
    #        DyF = DynamicFunction(DyC, name)

        
