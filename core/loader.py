#!/usr/bin/env python
## File: loader.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


#### System Includes #########################################################
import imp
import sys

#### Class:CoreHandler #######################################################
class coreHandler:
    class __impl:
        def __init__(self):
            self.command={}
            self.module_handler={}
		
        def AddTest(self, name):
            self.command[name] = True    
			
        def Load(self, CoreFile, paths):
            ## 
            try:
                ## check to see if we already have the module loaded
                return sys.modules[CoreFile]
            except KeyError:
                pass
                ## otherwise dont fail
            try:
                fp, filename, desc = imp.find_module(CoreFile, [paths])
            except ImportError:
                return False
            try:
                ## try to load it
                mod = imp.load_module(CoreFile, fp, filename, desc)
                self.module_handler[CoreFile] = mod
                try:
                    ## create an instance of that module
                    I = self.CreateInstance(mod)
                except Exception, e:
                    return e
                    ## return e if we fail
                try:
                    if len(e) <= 0:
                        ## see if we fail
                        return self.module_handler[CoreFile]
                except UnboundLocalError:
                    ## return the module that was loaded
                    return self.module_handler[CoreFile]
            finally:
                if fp:
                    ## close up the file handler
                    fp.close()
		
        def Unload(self, Module):
            ## remove the module
            self.module_handler[Module] = False
            return True
		
        def Reload(self, Module):
            ## reload a given module
            if self.GetModule(Module) == False:
                ## if the module isnt there
                return False
            else:
                ## otherwise reload the module
                reload(self.GetModule(Module))
                mod = self.module_handler[Module]
                try:
                    ## create a new instance of the module
                    I = self.CreateInstance(mod)
                except Exception, e:
                    pass
                return True
		  
        def GetModule(self, module):
            if self.module_handler.has_key(module):
                return self.module_handler[module]
            else:
                return False
				
        def MatchCoreFiles(self, CoreFile):
            if self.module_handler.has_key(CoreFile) == True:
                return CoreFile
            else:
                return False    
    
        def CreateInstance(self, Module):
            if self.GetModule(Module.__name__) != False:
                Dummy = getattr(Module,Module.__name__)
                D = Dummy()
                return D
            else:
                return False
				
        def ReloadInternal(self, Internal):
            if sys.modules.has_key(Internal):
                reload(Internal)
                return True
            else:
                return False
	
    __instance = None
    def __init__(self):
        if coreHandler.__instance is None:
            coreHandler.__instance = coreHandler.__impl()
            self.__dict__['_coreHandler__instance'] = coreHandler.__instance


    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
        
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)
