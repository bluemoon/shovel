import sys
import fnmatch


from core.loader       import coreHandler
from core.configurator import configurator
from core.debug        import *
from core.utils        import TermGreen
from core.utils        import TermEnd

import plugins as Plugins


def locate(pattern, root):
    for path, dirs, files in os.walk(root):
        for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
            yield filename
                    
def pathDifference(directory1, directory2):
    ''' accepts list input as in ['usr','home'] and ['usr','home','stuff']
        where the second input directory2 is the longer one.
    '''
    counter = 0
    while 1:
        try:
            if directory1[counter] == directory2[counter]:
                pass
            else:
                return directory2[counter:]
                break
                
        except IndexError:
            return directory2[counter:]
            break
            
        counter = counter + 1    
    
                
        
class plugin:
    def __init__(self):
        """dostring for __init__"""
        self.splitString = '.'
        self.config = configurator()
        
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
                cwd = os.getcwd()
                diff = pathDifference(cwd.split('/'), loadable.split('/'))
                diffList = ['shovel']
                ## so our list is only ['shovel'] currently
                for k in diff[1:-1]:                
                    diffList.append(k)
                    ## now append all of the elements in the path
                    ## list should be something like ['shovel','path','path']
                    
                    
                diffList.append(diff[-1:][0].split('.')[0])
                ## now append the last bit, stripped of the .py
                ## should be somethg like ['shovel','path','path','file']
                useString = '.'.join(diffList)
                ## concat it so
                ## 'shovel.path.path.file'
                debug(useString, DEBUG)
                ## print useString
                self.config.putFeature(useString)
                
