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
        
        
