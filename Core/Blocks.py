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
    ''' parses yaml '''
    def ParseBlock(self, yaml, reverse=False):
        ''' parses a block of yaml '''
        block = []
        if hasattr(yaml, 'keys'):
            for blocks in yaml.keys():
                block.append(blocks)
            if reverse:
                block.reverse()
            return block
