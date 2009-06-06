import core.api as api
requires = ['shovel.sys.builder','shovel.sys.downloader']

import plugins.sys.downloader as download

def run(*arguments):
    """run"""
    a = api.api()
    d = download.downloader()
    args = a.handleArguments(arguments)
    
    if args.has_key('link'):
        if args.has_key('md5'):
            d.http(args['link'], args['md5'])
        else:
            d.http(args['link'])

            
        
    c = cbuilder()
    c.build()
    
    

    
class cbuilder(object):
    def build(self):
        api.debug('debugging test!', api.DEBUG)
        
