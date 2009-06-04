import core.api as api

requires = ['shovel.sys.builder']

def run(*arguments):
	"""docstring for run"""
	c = cbuilder()
	c.build()

class cbuilder(object):
    def build(self):
        api.debug('debugging test!', api.DEBUG)
        
