class Singleton:
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state
		
class Configurator(Singleton):
	class __impl:
		def __init__(self):
			self.Packages = {}
			self.Modules = {}
			self.Features = []
			self.BigPackage = {}
			self.Globals = {}
			
		def GetGlobal(self,Global):
			if self.Globals.has_key(Global):
				return self.Globals[Global]
			else:
				return False
		def PutGlobal(self,Global,Value):
			self.Globals[Global] = Value
		def GetPackage(self,Package):
			return self.BigPackage[Package]
		def PutPackage(self,Package,Yaml):
			self.BigPackage[Package] = Yaml
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
		def deleteModuleLoaded(self):
			pass
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

def feature(args):
		#self.putFeature(Feature)
		def _feature(*kw):
			print kw
			return kw
		return _feature
		
	
		