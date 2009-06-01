import core.configurator as config

from core.debug import debug
ERROR   = -1
NONE    = 0
WARNING = 1
INFO    = 2
DEBUG   = 3

from core.utils import pprint

import core.file as _file

class api(object):
    class file(object):
        def touch(self, file_):
            assert file_, "no file variable passed, or value is None"
            _file.touch(file_)
            
        def chdir(self, directory):
            assert directory, "no directory variable passed, or value is None"
            _file.chdir(directory)
            
        def buildPath(self, base, *path):
            assert base, "no base variable passed, or value is None"
            assert path, "no path variable passed, or value is None"
            _file.buildPath(base, path)   
            
        def mkdirIfAbsent(self, *arguments):
            assert arguments, "no argument variable passed, or value is None"
            _file.mkdirIfAbsent(arguments)
        def rmDirectoryRecursive(self, path):
            assert path, "no path variable passed, or value is None"
            
            
    class config(object):
        def __init__(self):
            self.config = config.Configurator()
        def getGlobal(self, glbal):
            assert glbal, "there was no global input"
            self.config.GetGlobal(glbal)
    
        def putGlobal(self, glbal, value):
            """docstring for putGlobal"""
            assert glbal, "there was no global input"
            assert value, "there was no value"
        
            self.config.PutConfig(glbal, value)
        
    def debug(self, string, level=NONE):
        assert string, "there is no debug string"
        debug(string, level)
    
    def pprint(self, string, label, color=None, labelColor=None):
        assert string, "there is no string value, or it is None!"
        assert lable,  "there is no label or it is None!"
        pprint(string, label, color, labelColor)
        