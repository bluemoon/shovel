from core.debug import *
import imp

class recipe(object):
    def runner(self, recipeName, recipeLocation):
    	''' runner, arguments: recipeLocation '''
		try:
			module = sys.modules[recipeName]
		except KeyError:	
		    file, pathname, description = imp.find_module(recipeName, recipeLocation)
            debug('%s %s %s %s' % (recipeName, file, pathname, description))
            module = imp.load_module(recipeName, file, pathname, description)
            
