import core.configurator as config

from core.debug import debug
ERROR   = -1
NONE    = 0
WARNING = 1
INFO    = 2
DEBUG   = 3

from core.utils import pprint
from core.type import accepts
from core.dependencies import dependencies

import core.file as _file

class api(object):
    ''' this is the plugin api '''
    class dependencies(object):
        def __init__():
            self.deps = dependencies()
        
        def add(dependant, dependsOn=None):
            self.deps.depGenAdd(self, dependant, dependsOn)
        
        def resolve(self):
            self.deps.dependencyGenRun()
            
    class file(object):
        ''' this is a subclass to the api for all of the file  '''    
        @accepts('file_', str)
        def touch(self, file_):
            ''' touch a file, like the unix command touch
                arguments: file_ -- the file/path to file to be changed
            '''
            assert file_, "no file variable passed, or value is None"
            _file.touch(file_)
            
        @accepts('directory', str)
        def chdir(self, directory):
            ''' change to a directory and emit debugging code.
                arguments: directory -- the directory you want to change to
            '''
            assert directory, "no directory variable passed, or value is None"
            _file.chdir(directory)
            
        @accepts('base', str)
        ## @accepts('path', list)    
        def buildPath(self, base, *path):
            ''' assemble a path based on the base path. 
                arguments: 
                    base -- the base path 
                    *path -- list input that adds the path to the base path
            '''
            assert base, "no base variable passed, or value is None"
            assert path, "no path variable passed, or value is None"
            _file.buildPath(base, path)
            
        ## @accepts('arguments', list)
        def mkdirIfAbsent(self, *arguments):
            ''' creates a folder if it isnt already present 
                arguments: arguments -- the folder you want to be created in list form
            '''
            
            assert arguments, "no argument variable passed, or value is None"
            _file.mkdirIfAbsent(arguments)
            
        @accepts('path', str)    
        def rmDirectoryRecursive(self, path):
            assert path, "no path variable passed, or value is None"
            
            
    class config(object):
        ''' this is a subclass to the api for all of the config methods '''
        def __init__(self):
            self.config = config.Configurator()
            
        def getGlobal(self, glbal):
            ''' retrieves a global variable from storage. '''
            assert glbal, "there was no global input"
            self.config.GetGlobal(glbal)
    
        def putGlobal(self, glbal, value):
            ''' puts a global variable in storage so that it
                can be retrieved from anywhere in the code '''
            assert glbal, "there was no global input"
            assert value, "there was no value"
        
            self.config.PutConfig(glbal, value)
        
    def debug(self, string, level=NONE):
        ''' this prints debugging code in a fashionable way. '''
        assert string, "there is no debug string"
        debug(string, level)
    
    def pprint(self, string, label, color=None, labelColor=None):
        ''' formats the code so that the string is on the left and 
            the label goes on the right side. with padding in the center
        '''
        assert string, "there is no string value, or it is None!"
        assert lable,  "there is no label or it is None!"
        pprint(string, label, color, labelColor)
        
    def handleArguments(self, arguments):
        argumentDict = {}
        for a in self._arg_gen(arguments):
            debug(a, DEBUG)
            argumentDict.update(a)
                
        return argumentDict
                
    def _arg_gen(self, args):
        for a in args:
            for b in a:
                if isinstance(b, list):
                    for c in b:
                        yield c
                else:
                   yield b
