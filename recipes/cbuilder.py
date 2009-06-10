import core.api as api
requires = ['shovel.sys.builder','shovel.sys.downloader']

import plugins.sys.downloader as download

def isTar(filename):
    if 'tar' in filename:
        return True
    else:
        return False

def isZip(filename):
    if 'zip' in filename:
        return True
    else:
        return False
        
def run(*arguments):
    """run"""
    
    a = api.api()
    args = a.handleArguments(arguments)
    
    if args.has_key('link'):
        download.http_download(args['link'], 'tmp/downloads')
        if isTar(args['link']):
            pass
        
    c = cbuilder()
    c.build()
    
    

    
class cbuilder(object):
    def build(self):
        api.debug('debugging test!', api.DEBUG)
        
