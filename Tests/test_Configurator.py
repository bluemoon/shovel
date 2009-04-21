import libpry
import sys

class TestConfigurator(libpry.AutoTree):
	def setUp(self):
		sys.path.append('../')
		from Core.Configurator import Configurator
		self.Config = Configurator()
	
	def test_ConfiguratorPutFeature(self):
		self.Config.putFeature('feature')
		assert self.Config.getFeature('feature') == True
	
	def test_ConfiguratorPutGlobal(self):
		self.Config.PutGlobal('g1',True)
		assert self.Config.GetGlobal('g1') == True
	
	def test_ConfiguratorPutPackage(self):
		self.Config.PutPackage('p1',True)
		assert self.Config.GetPackage('p1') == True
	
	def test_ConfiguratorPutConfig(self):
		self.Config.PutConfig('c1',True)
		assert self.Config.GetConfig('c1') == True	
	
	def test_ConfiguratorGlobalInstances(self):
		sys.path.append('../Core/')
		from Core.Configurator import Configurator
		Config = Configurator()
		Config.PutGlobal('c1',True)
		assert self.Config.GetGlobal('c1') == True
		
	def test_ConfiguratorGlobalFeature(self):
		sys.path.append('../Core/')
		from Core.Configurator import Configurator
		Config = Configurator()
		Config.putFeature('c1')
		assert self.Config.getFeature('c1') == True
	
	def test_ConfiguratorGlobalPackage(self):
		sys.path.append('../Core/')
		from Core.Configurator import Configurator
		Config = Configurator()
		Config.PutPackage('p1',True)
		assert self.Config.GetPackage('p1') == True
	
	def test_ConfiguratorGlobalConfig(self):
		sys.path.append('../Core/')
		from Core.Configurator import Configurator
		Config = Configurator()
		Config.PutConfig('p1',True)
		assert self.Config.GetConfig('p1') == True
		
tests = [
	TestConfigurator()
]