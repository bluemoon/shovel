#!/usr/bin/env python
## 
import unittest
import sys

class TestCoreDependencies(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from Core.Dependencies import Dependencies
        self.depend = Dependencies()
    def test_1_letter_orderDependencies(self):
        self.depend.depGenAdd('a')
        self.depend.depGenAdd('b','a')
        self.depend.depGenAdd('c','b')
        self.depend.depGenAdd('d','b')
        
        deps = self.depend.dependencyGenRun()
        
        assert deps == [set(['a']), set(['b']), set(['c', 'd'])]
    
    def test_2_numerical_orderDependencies(self):
        self.depend.depGenAdd(1)
        self.depend.depGenAdd(2, 1)
        self.depend.depGenAdd(3, 1)
        self.depend.depGenAdd(4, 3)
        
        deps = self.depend.dependencyGenRun()
        
        assert deps == [set([1]), set([2, 3]), set([4])]
    
    def test_3_word_orderDependencies(self):
        self.depend.depGenAdd('one')
        self.depend.depGenAdd('two',   'one')
        self.depend.depGenAdd('three', 'two')
        
        deps = self.depend.dependencyGenRun()
        
        assert deps == [set(['one']), set(['two']), set(['three'])]
    
    def test_4_BuildCoreDependencies(self):
        core = {'1':[],'2':'1','3':'2'}    
        self.depend.buildCoreDeps(core)
        deps = self.depend.dependencyGenRun()
        assert deps == [set(['1']), set(['2']), set(['3'])]