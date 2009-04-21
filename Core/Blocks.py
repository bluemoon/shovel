
class Blocks(object):
	def ParseBlock(self,Yaml,Reverse=False):
		Block = []
		if hasattr(Yaml, 'keys'):
			for Blocks in Yaml.keys():
			 	Block.append(Blocks)
		if Reverse:
			Block.reverse()
		return Block