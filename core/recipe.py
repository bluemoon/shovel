from core.debug import *
from core.configurator import configurator

import imp
import sys

import recipes

class recipe(object):
    def __init__(self):
        self.runFunction = 'run'
        self.config = configurator()
        
    def runner(self, recipeName, *arguments):
        ''' runner, arguments: recipeLocation '''
        try:
            module = sys.modules['recipes.' + recipeName]
        except KeyError:
            __import__('recipes.' + recipeName)
            module = sys.modules['recipes.' + recipeName]
            
        ## if the recipe has requirements
        if 'requires' in module.__dict__ and isinstance(module.__dict__['requires'], list):
            for reqs in  module.__dict__['requires']:
                if self.config.getFeature(reqs):
                    debug('feature %s available' % (reqs), DEBUG)
                else:
                    debug('feature %s unavailable' % (reqs), DEBUG)
                    print 'plugin %s not available, exiting gracefully...' %  (reqs)
                    sys.exit(-1)
        
        ## run the run function, run()    
        for function in module.__dict__:
            if function == self.runFunction:
                attr = getattr(module, self.runFunction)
                out = attr(arguments)
