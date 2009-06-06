#!/usr/bin/env python 
import unittest
import sys

sys.path.append('../')
from core.exceptions import FeatureError

class TestCoreFeatures(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from core.features import features
        self.feat = features()
        self.testString = 'shovel.pbuilder.build'
        
    def test_1_splitByClass(self):
        builder = self.feat.splitByClass(self.testString)
        assert builder == 'shovel.pbuilder'
        
    def test_2_splitClass(self):
        builder = self.feat.splitClass(self.testString)
        assert builder == 'pbuilder'
        
    def test_3_splitFunction(self):
        builder = self.feat.splitFunction(self.testString)
        assert builder == 'build'
