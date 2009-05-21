import unittest
import sys

class TestBlocks(unittest.TestCase):
    def setUp(self):
        sys.path.append('../')
        from Core.Blocks import Blocks
        from Core.Dirt   import Dirt
        
        self.Blocks = Blocks()
        self.Dirt   = Dirt()
        
    def test_os_reverse_Blocks(self):
        Dirt = self.Dirt.loadDirt()
        Blocks = self.Blocks.ParseBlock(Dirt,True)
        assert Blocks == ['Linux','Darwin']
        
    def test_os_Blocks(self):
        Dirt = self.Dirt.loadDirt()
        Blocks = self.Blocks.ParseBlock(Dirt)
        assert Blocks == ['Darwin','Linux']
        
    def test_os_SubBlocks(self):
        dirt = self.Dirt.loadDirt()
        blocks = self.Blocks.ParseBlock(dirt['Linux'])
        assert blocks == ['pre.flight', 'build']