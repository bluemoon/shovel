## File: Features.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


class features(object):

    ### For searches ###
    def splitByClass(self, Search):
        Temp = Search.split(".")
        return ".".join(Temp[:2])

    def splitClass(self, Search):
        Temp = Search.split(".")
        return Temp[1:2][0]

    def splitFunction(self, Search):
        Temp = Search.split(".")
        return Temp[-1:][0]
        
