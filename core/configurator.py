##############################################################################
## File: Configurator.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### Class:Configurator ######################################################
class Configurator:
    class __impl:
        def __init__(self):
            self.packages   = {}
            self.modules    = {}
            self.features   = []
            self.bigPackage = {}
            self.globals    = {}
            self.out        = {}
        
        ## rename to getAllOut
        def GetAllOut(self):
            return self.out

        def GetOutYaml(self, gYaml):
            if self.out.has_key(gYaml):
                return self.out[gYaml]
            else:
                return False
            
        def CreateOutYaml(self, gYaml):
            self.out[gYaml] = []
            return self.out[gYaml]
            
        def AppendOutYaml(self, gYaml, value):
            if not self.out.has_key(gYaml):
                self.CreateOutYaml(gYaml)
                
            self.out[gYaml].append(value)
            
        def GetGlobal(self, glbl):
            if self.globals.has_key(glbl):
                return self.globals[glbl]
            else:
                return False

        def PutGlobal(self, glbl, value):
            self.globals[glbl] = value
        
        def getGlobalDump(self):
            return self.globals

        def setGlobalDump(self, yaml):
            self.globals = yaml

        def GetPackage(self, package):
            return self.bigPackage[package]
        
        def PutPackage(self, package, yaml):
            self.bigPackage[package] = yaml

        def FindInPackage(self, search, package):
            for lots in self.bigPackage[package]:
                if hasattr(lots,'keys'):
                    if lots.has_key(search):
                        return lots[search]

        def GetConfig(self, package):
            return self.packages[package]

        def PutConfig(self, package, yaml):
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
        if Configurator.__instance is None:
            Configurator.__instance = Configurator.__impl()
            self.__dict__['_Configurator__instance'] = Configurator.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)	

	
		
