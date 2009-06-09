import unittest
import mox

import core.plugin as plugin

class TestCorePlugin(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_1_pathDifference(self):
        output = plugin.pathDifference(['home','bluemoon'],['home','bluemoon','desktop','stuff'])
        assert output == ['desktop','stuff']
        
    def test_2_pathDifference(self):
        output = plugin.pathDifference(['home','bluemoon','desktop','stuff'], ['home','bluemoon'])
        assert output == []
    
    def test_3_plugin(self):
        p = plugin.plugin()
        self.mox.StubOutWithMock(p.config, 'putFeature')
        p.config.putFeature()

        self.mox.ReplayAll()        
        p.getAll()

        

