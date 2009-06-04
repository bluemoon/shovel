from core.debug import *

import imp
import sys

import recipes.cbuilder

class recipe(object):
    def __init__(self):
        self.runFunction = 'run'
        
    def runner(self, recipeName, recipeLocation, *arguments):
        ''' runner, arguments: recipeLocation '''
        try:
            module = sys.modules['recipes.' + recipeName]
        except KeyError:	
            ## ImportError: No frozen submodule named recipes.cbuilder
            ## file, pathname, description = imp.find_module(recipeName, recipeLocation)
            ## debug('%s %s %s %s' % (recipeName, file, pathname, description), DEBUG)
            ## module = imp.load_module(recipeName, file, pathname, description)
            pass
            
        for function in module.__dict__:
            if function == self.runFunction:
                attr = getattr(module, self.runFunction)
                out = attr(arguments)
