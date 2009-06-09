import unittest

import core.plugin

class TestCorePlugin(unittest.TestCase):
    def test_1_pathDifference(self):
        output = core.plugin.pathDifference(['home','bluemoon'],['home','bluemoon','desktop','stuff'])
        assert output == ['desktop','stuff']
        
    def test_2_pathDifference(self):
        output = core.plugin.pathDifference(['home','bluemoon','desktop','stuff'], ['home','bluemoon'])
        assert output == []
