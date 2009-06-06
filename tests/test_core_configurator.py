import unittest
import mox
import sys

class TestConfigurator(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from core.configurator import configurator
        self.Config = configurator()

    def test_1_ConfiguratorPutFeature(self):
        self.Config.putFeature('feature')
        assert self.Config.getFeature('feature') == True

    def test_2_ConfiguratorPutGlobal(self):
        self.Config.putGlobal('g1',True)
        assert self.Config.GetGlobal('g1') == True

    def test_3_ConfiguratorPutPackage(self):
        self.Config.putPackage('p1',True)
        assert self.Config.GetPackage('p1') == True

    def test_4_ConfiguratorPutConfig(self):
        self.Config.putConfig('c1',True)
        assert self.Config.GetConfig('c1') == True	

    def test_5_ConfiguratorGlobalInstances(self):
        sys.path.append('../Core/')
        from core.configurator import configurator
        Config = configurator()
        Config.putGlobal('c1', True)
        assert self.Config.getGlobal('c1') == True

    def test_6_ConfiguratorGlobalFeature(self):
        sys.path.append('../core/')
        from core.configurator import configurator
        Config = configurator()
        Config.putFeature('c1')
        assert self.Config.getFeature('c1') == True

    def test_7_ConfiguratorGlobalPackage(self):
        sys.path.append('../core/')
        from core.configurator import configurator
        Config = configurator()
        Config.putPackage('p1',True)
        assert self.Config.getPackage('p1') == True

    def test_8_ConfiguratorGlobalConfig(self):
        sys.path.append('../core/')
        from core.configurator import configurator
        Config = configurator()
        Config.putConfig('p1', True)
        assert self.Config.getConfig('p1') == True
        
    def test_9_false_ConfiguratorGetOutYaml(self):
        yaml = self.Config.getOutYaml('feature')
        assert yaml == False
        
    def test_a10_ConfiguratorCreateOutYaml(self):
        yaml = self.Config.createOutYaml('feature')
        test = []
        assert yaml == test
        
    def test_a11_ConfiguratorAppendOutYaml(self):
        self.Config.appendOutYaml('global','value')
        outYaml = self.Config.getOutYaml('global')
        assert outYaml == ['value']
        
    def test_a12_Configurator_putModuleLoaded(self):
        modules = self.Config.putModuleLoaded('Module')
        assert modules == {'Module': []}
        
    def test_a13_Configurator_deleteModuleLoaded(self):
        out = self.Config.deleteModuleLoaded('Module')
        assert out == True
        
