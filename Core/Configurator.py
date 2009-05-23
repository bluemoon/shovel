##############################################################################
## File: Configurator.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################
import Core.singleton

#### Class:Configurator ######################################################
class Configurator(singleton.Singleton):
    class __impl:
        def __init__(self):
            self.Packages   = {}
            self.Modules    = {}
            self.Features   = []
            self.BigPackage = {}
            self.Globals    = {}
            self.Out        = {}
        
        def GetAllOut(self):
            return self.Out

        def GetOutYaml(self,Global):
            if self.Out.has_key(Global):
                return self.Out[Global]
            else:
                return False
            
        def CreateOutYaml(self,Global):
            self.Out[Global] = []
            return self.Out[Global]
            
        def AppendOutYaml(self,Global,Value):
            if not self.Out.has_key(Global):
                self.CreateOutYaml(Global)
            self.Out[Global].append(Value)
            
        def GetGlobal(self,Global):
            if self.Globals.has_key(Global):
                return self.Globals[Global]
            else:
                return False

        def PutGlobal(self,Global,Value):
            self.Globals[Global] = Value
        
        def getGlobalDump(self):
            return self.Globals

        def setGlobalDump(self,yaml):
            self.Globals = yaml

        def GetPackage(self,Package):
            return self.BigPackage[Package]
        
        def PutPackage(self,Package,Yaml):
            self.BigPackage[Package] = Yaml

        def FindInPackage(self,Search,Package):
            for Lots in self.BigPackage[Package]:
                if hasattr(Lots,'keys'):
                    if Lots.has_key(Search):
                        return Lots[Search]

        def GetConfig(self,Package):
            return self.Packages[Package]

        def PutConfig(self,Package,Yaml):
            self.Packages[Package] = Yaml

        def getModuleLoaded(self,Module):
            for FindModule in self.Modules.keys():
                if FindModule == Module:
                    return Module

        def putModuleLoaded(self,Module):
            self.Modules[Module] = []
            return self.Modules
        
        def deleteModuleLoaded(self,Module):
            return True

        def getFeature(self,Feature):
            for F in self.Features:
                if F == Feature:
                    return True

        def deleteFeature(self,Feature):
            pass
        
        def putFeature(self,Fture):
            self.Features.append(Fture)
            return self.Features

    __instance = None
    def __init__(self):
        if Configurator.__instance is None:
            Configurator.__instance = Configurator.__impl()
            self.__dict__['_Configurator__instance'] = Configurator.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)	

	
		
