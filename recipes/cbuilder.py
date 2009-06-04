import core.api

requires = ['shovel.sys.builder']

def run(*arguments):
	"""docstring for run"""
	c = cbuilder()
	c.build()

class cbuilder(object):
    def build(self):
        pass
