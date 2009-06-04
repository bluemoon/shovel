##############################################################################
## File: Configurator.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

class configurator:
    class __impl:
        def __init__(self):
            self.packages   = {}
            self.modules    = {}
            self.features   = []
            self.bigPackage = {}
            self.globals    = {}
            self.out        = {}
        
        ## rename to getAllOut
        def getAllOut(self):
            return self.out

        def getOutYaml(self, gYaml):
            if self.out.has_key(gYaml):
                return self.out[gYaml]
            else:
                return False
            
        def createOutYaml(self, gYaml):
            self.out[gYaml] = []
            return self.out[gYaml]
            
        def appendOutYaml(self, gYaml, value):
            if not self.out.has_key(gYaml):
                self.CreateOutYaml(gYaml)
                
            self.out[gYaml].append(value)
            
        def getGlobal(self, glbl):
            if self.globals.has_key(glbl):
                return self.globals[glbl]
            else:
                return False

        def putGlobal(self, glbl, value):
            self.globals[glbl] = value
        
        def getGlobalDump(self):
            return self.globals

        def setGlobalDump(self, yaml):
            self.globals = yaml

        def getPackage(self, package):
            return self.bigPackage[package]
        
        def putPackage(self, package, yaml):
            self.bigPackage[package] = yaml

        def findInPackage(self, search, package):
            for lots in self.bigPackage[package]:
                if hasattr(lots,'keys'):
                    if lots.has_key(search):
                        return lots[search]

        def getConfig(self, package):
            return self.packages[package]

        def putConfig(self, package, yaml):
            self.packages[package] = yaml

        def getModuleLoaded(self, module):
            for findModule in self.modules.keys():
                if findModule == module:
                    return module

        def putModuleLoaded(self, module):
            self.modules[module] = []
            return self.modules
        
        def deleteModuleLoaded(self, module):
            return True

        def getFeature(self, feature):
            for feat in self.features:
                if feat == feature:
                    return True

        def deleteFeature(self, feature):
            pass
        
        def putFeature(self, feature):
            self.features.append(feature)
            return self.features

    __instance = None
    def __init__(self):
        if configurator.__instance is None:
            configurator.__instance = configurator.__impl()
            self.__dict__['_configurator__instance'] = configurator.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)	

	
		
