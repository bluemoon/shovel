## File: configurator.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


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
        #def getAllOut(self):
        #    ''' returns an internal storage object'''
        #    return self.out

        #def getOutYaml(self, gYaml):
        #    ''' outputs yaml otherwise returns false '''
        #    if self.out.has_key(gYaml):
        #        return self.out[gYaml]
        #    else:
        #        return False
            
        #def createOutYaml(self, gYaml):
        #    ''' creates an internal dictionary for storage '''
        #    self.out[gYaml] = []
        #    return self.out[gYaml]
            
        #def appendOutYaml(self, gYaml, value):
        #    ''' appends to the internal dictionary '''
        #    if not self.out.has_key(gYaml):
        #        self.CreateOutYaml(gYaml)
        #        
        #    self.out[gYaml].append(value)
            
        def getGlobal(self, glbl):
            ''' gets a global from the internal dictionary '''
            if self.globals.has_key(glbl):
                return self.globals[glbl]
            else:
                return False

        def putGlobal(self, glbl, value):
            ''' put a global in storage '''
            self.globals[glbl] = value
        
        def getGlobalDump(self):
            ''' get a dump of the global dictionary  '''
            return self.globals

        def setGlobalDump(self, yaml):
            ''' allows a dump of a dictionary into the internal object'''
            self.globals = yaml

        #def getPackage(self, package):
        #    ''' get a package from the dict '''
        #    return self.bigPackage[package]
        # 
        #def putPackage(self, package, yaml):
        #    ''' inserts a package into the dict '''
        #    self.bigPackage[package] = yaml

        #def findInPackage(self, search, package):
        #   ''' do we have the dict? '''
        #    for lots in self.bigPackage[package]:
        #        if hasattr(lots,'keys'):
        #            if lots.has_key(search):
        #                return lots[search]

        #def getConfig(self, package):
        #    ''' get the config from the internal dictionary '''
        #    return self.packages[package]

        #def putConfig(self, package, yaml):
        #    ''' put a config in the internal dictionary'''
        #   self.packages[package] = yaml

        #def getModuleLoaded(self, module):
        #    ''' return a module that has been loaded '''
        #    for findModule in self.modules.keys():
        #        if findModule == module:
        #            return module

        #def putModuleLoaded(self, module):
        #    ''' put a module in the internal dictionary '''
        #    self.modules[module] = []
        #    return self.modules
        
        #def deleteModuleLoaded(self, module):
        #    return True

        def getFeature(self, feature):
            ''' check to see if there is a feature '''
            for feat in self.features:
                if feat == feature:
                    return True

        #def deleteFeature(self, feature):
        #    pass
        
        def putFeature(self, feature):
            ''' put a feature in the internal dictionary '''
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

	
		
