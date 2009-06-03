import os
import sys
import fnmatch


from core.loader       import CoreHandler
from core.configurator import configurator
from core.debug        import *
from core.terminal import TermGreen
from core.terminal import TermEnd

import plugins as Plugins



'''plugins = {
    'shovel':{
        'systools' : {
            'builder':{
                'waf' :['configure','build'],
                'make':['configure','build'],
                
            },
            'downloader':{
                'http': ['download'],
                'svn' : ['checkout',]
            }
        }
        
    }
} '''

def locate(pattern, root):
            for path, dirs, files in os.walk(root):
                for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
                    yield filename
                    
def alignDirectories(directory1, directory2):
    for path in directory1:
        for path2 in directory2:
            if not path == path2:
                break
                
        
class plugin:
    def __init__(self):
        """dostring for __init__"""
        self.splitString = '.'
       
    def getAll(self):
        import plugins
        ''' gets all of the plugins '''
        rPath =  plugins.__dict__['__path__'][0]
        ## it should turn out something like
        ## shovel.sys.http.download => [plugins]/sys/http.py[function:download]
        for loadable in locate('*.py', rPath):
            pyElement = loadable.split('/')[-1:]
            ## i only want the end element
            if pyElement[0] != '__init__.py':
                print loadable
            
            cwd = os.getcwd()
            listDirectory = cwd.split('/')
            
                
            
        
        
class Plugin:
    def __init__(self):
        self.loader = CoreHandler()
        self.config = configurator()
	
    def loadAll(self, folder=None):
        Dir = os.path.join(os.path.dirname(__file__)).split("/")[:-2]
        for Py in locate("*.py", Plugins.__dict__['__path__'][0]):
            self.loadAbsolute(Py)

    def loadAbsolute(self, absPath):
        absSplit = absPath.split('/')
        file = absSplit[-1:]
        nFile = file[0].split(".") 
        module = self.load(nFile[0],"/".join(absSplit[:-1]))
        self.config.putModuleLoaded(nFile[0])

    def load(self, name=None, folder=None):
        self.config.putFeature('shovel.'+name.lower())
        self.loader.Load(name,folder)
        loader = self.loader.GetModule(name)
        try:
            if name != "__init__":
                for Function in loader.__dict__[name].__dict__:
                    if Function[0:2] != '__':
                        self.config.putFeature('shovel.'+name.lower()+"." +Function)
                        debug('Loaded: '+ TermGreen +'shovel.'+name.lower()+"." +Function + TermEnd,INFO)

        except AttributeError:
            pass

