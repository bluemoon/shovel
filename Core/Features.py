from Core.Loader       import CoreHandler
from Core.Configurator import Configurator

class Features(object):
	def __init__(self):
		self.Loader = CoreHandler()
		self.Config = Configurator()
	### For searches ###
	def SplitByClass(self,Search):
		Temp = Search.split(".")
		return ".".join(Temp[:2])
	def SplitClass(self,Search):
		Temp = Search.split(".")
		return Temp[1:2][0]
	def SplitFunction(self,Search):
		Temp = Search.split(".")
		return Temp[-1:][0]
	### End Searches ###
	def RunFeature(self,Feature,Name):
		if hasattr(Feature, 'keys'):
			for Use in Feature.keys():
				if Use == 'use':
					Module = self.Loader.GetModule(self.SplitClass(Feature[Use]))
					if hasattr(Module,self.SplitClass(Feature[Use])):
						self.Config.PutConfig(Name,Feature)
						DynamicClass = getattr(Module,self.SplitClass(Feature[Use]))
						DyC = DynamicClass()
						DynamicFunction = getattr(DynamicClass,self.SplitFunction(Feature[Use]))
						DyF = DynamicFunction(DyC,Name)
						
		else:
			pass
