#!/usr/bin/env python
##############################################################################
## File: Dirt.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Includes #########################################################
import os
import yaml

#### Class:Dirt ##############################################################
class Dirt(object):
    def dirtExists(self,file="dirt"):
        """ Check to see if the dirt file exists"""
        if os.path.exists(file):
            return True
        else:
            return False
        
    def loadDirt(self):
        """ Load the dirt File """
        dirtFile = open('dirt', 'r')
        dFile = dirtFile.read()
        g_Yaml = yaml.load(dFile)
        return g_Yaml
