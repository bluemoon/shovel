#!/usr/bin/env python
import unittest
import sys

from Core.Exceptions import FeatureError

class TestCoreFeatures(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from Core.Features import Features
        self.feat = Features()
        self.testString = 'shovel.pbuilder.build'
        
    def test_1_splitByClass(self):
        builder = self.feat.SplitByClass(self.testString)
        assert builder == 'shovel.pbuilder'
        
    def test_2_splitClass(self):
        builder = self.feat.SplitClass(self.testString)
        assert builder == 'pbuilder'
        
    def test_3_splitFunction(self):
        builder = self.feat.SplitFunction(self.testString)
        assert builder == 'build'
    
    def test_4_fail_RunFeature(self):
        self.assertRaises(FeatureError, self.feat.RunFeature, False, False)