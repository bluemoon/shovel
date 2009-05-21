import unittest
import sys

class TestDirt(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from Core.Dirt import Dirt
        self.Dirt = Dirt()
    def test_dirtExists(self):
        assert self.Dirt.dirtExists() == True   
    def test_false_dirtExists(self):
        assert self.Dirt.dirtExists('non-exist') == False
    def test_loadDirt(self):
        assert self.Dirt.loadDirt() != False or self.Dirt.loadDirt() != None