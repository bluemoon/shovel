import libpry
import sys

sys.path.append('../')
sys.path.append('Plugins/')

class TestDirt(libpry.AutoTree):
	def setUp(self):
		sys.path.append('../Core/')
		from shovel import Dirt
		self.Dirt = Dirt()
	def test_dirtExists(self):
		assert self.Dirt.dirtExists() == True
	def test_loadDirt(self):
		assert self.Dirt.loadDirt() != False or self.Dirt.loadDirt() != None
class TestBlocks(libpry.AutoTree):
	def setUp(self):
		sys.path.append('../Core/')
		from shovel import Blocks, Dirt
		self.Blocks = Blocks()
		self.Dirt = Dirt()
	def test_Blocks(self):
		Dirt = self.Dirt.loadDirt()
		assert self.Blocks.ParseBlock(Dirt) == ['pre.flight', 'dist', 'build']
		
		
tests = [
	TestDirt(),
	TestBlocks()
]
