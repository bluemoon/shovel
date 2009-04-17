class Configurator(object):
	def __init__(self):
		self.Packages = {}
		self.Modules = {}
		self.Features = []
	def GetConfig(self,Package):
		return self.Packages[Package]
	def PutConfig(self,Package,Yaml):
		self.Packages[Package] = Yaml
	def getModuleLoaded(self,Module):
		for FindModule in self.Modules.keys():
			if FindModule == Module:
				return Module
	def putModuleLoaded(self,Module,Handle):
		pass
	def deleteModuleLoaded(self):
		pass
	def getFeature(self,Feature):
		if Feature in self.Features:
			return True
		else:
			return False
	def deleteFeature(self,Feature):
		pass
	def putFeature(self,Fture):
		self.Features.append(Fture)
		return True
		
class feature(object):
	def __init__(self,Feature):
		#self.putFeature(Feature)
		pass
	def __call__(self,Feature):
		pass
	
		