import unittest
import sys

class TestConfigurator(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from Core.Configurator import Configurator
        self.Config = Configurator()

    def test_1_ConfiguratorPutFeature(self):
        self.Config.putFeature('feature')
        assert self.Config.getFeature('feature') == True

    def test_2_ConfiguratorPutGlobal(self):
        self.Config.PutGlobal('g1',True)
        assert self.Config.GetGlobal('g1') == True

    def test_3_ConfiguratorPutPackage(self):
        self.Config.PutPackage('p1',True)
        assert self.Config.GetPackage('p1') == True

    def test_4_ConfiguratorPutConfig(self):
        self.Config.PutConfig('c1',True)
        assert self.Config.GetConfig('c1') == True	

    def test_5_ConfiguratorGlobalInstances(self):
        sys.path.append('../Core/')
        from Core.Configurator import Configurator
        Config = Configurator()
        Config.PutGlobal('c1',True)
        assert self.Config.GetGlobal('c1') == True

    def test_6_ConfiguratorGlobalFeature(self):
        sys.path.append('../Core/')
        from Core.Configurator import Configurator
        Config = Configurator()
        Config.putFeature('c1')
        assert self.Config.getFeature('c1') == True

    def test_7_ConfiguratorGlobalPackage(self):
        sys.path.append('../Core/')
        from Core.Configurator import Configurator
        Config = Configurator()
        Config.PutPackage('p1',True)
        assert self.Config.GetPackage('p1') == True

    def test_8_ConfiguratorGlobalConfig(self):
        sys.path.append('../Core/')
        from Core.Configurator import Configurator
        Config = Configurator()
        Config.PutConfig('p1',True)
        assert self.Config.GetConfig('p1') == True
        
    def test_9_false_ConfiguratorGetOutYaml(self):
        yaml = self.Config.GetOutYaml('feature')
        assert yaml == False
        
    def test_a10_ConfiguratorCreateOutYaml(self):
        yaml = self.Config.CreateOutYaml('feature')
        test = []
        assert yaml == test
        
    def test_a11_ConfiguratorAppendOutYaml(self):
        self.Config.AppendOutYaml('global','value')
        outYaml = self.Config.GetOutYaml('global')
        assert outYaml == ['value']
        
    def test_a12_Configurator_putModuleLoaded(self):
        modules = self.Config.putModuleLoaded('Module')
        assert modules == {'Module': []}
        
    def test_a13_Configurator_deleteModuleLoaded(self):
        out = self.Config.deleteModuleLoaded('Module')
        assert out == True
        
