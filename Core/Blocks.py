##############################################################################
## File: Blocks.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### Class:Blocks ############################################################
class Blocks(object):
	def ParseBlock(self,Yaml,Reverse=False):
		Block = []
		if hasattr(Yaml, 'keys'):
			for Blocks in Yaml.keys():
			 	Block.append(Blocks)
		if Reverse:
			Block.reverse()
		return Block