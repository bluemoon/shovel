#!/usr/bin/env python
##############################################################################
## File: File.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Includes #########################################################
import os

def rmDirectoryRecursive(Path):
	for I in os.listdir(Path):
		FullPath = Path + "/" + I
		if os.path.isdir(FullPath):
			rmDirectoryRecursive(FullPath)
		else:
			os.remove(FullPath)
	os.rmdir(Path)