## This is the pbuilder. or package builder
from Core.Configurator import Configurator

import builder
import downloader
import extractor
import patcher

class pbuilder(object):
  def __init__(self):
    self.config = Configurator()
    
    
  def build(self, name):
    config = self.config.GetConfig(name)
    filename = config["link"].split("/")[-1:][0]
    
    configuration = config['configure']
    
    try:
        md5 = config["md5"]
    except Exception, E:
        md5 = None
    
    d = downloader.downloader()
    d.http(name)
    if md5:
        digest = downloader.md5("tmp/downloads/" + filename, md5)
        if digest == True:
            print '[md5]: %s digests match. download fine. ' % (md5)
        else:
            print 'Digest failed got: %s expected: %s' % (digest, md5)
            raise Exception('md5DigestError') 
    
    print filename
    
    '''
    
    
    Configuration = Config['configure']
    try:
      Md5 = Config["md5"]
    except Exception, E:
		  Md5 = None
		  
    d = downloader()
    d.http(Name)
    
    if Md5:
      Digest = md5("tmp/downloads/" + Filename,Md5)
      if Digest == True:
        print '[md5]: %s digests match. download fine. ' % (Md5)
      else:
        print 'Digest failed got: %s expected: %s' % (Digest,Md5)
        raise Exception('md5DigestError') 
        
    e = extractor()
    e.tar(Filename,Name)
    Folder = ExtractNameFromTar(Filename)
    
    debug('Adding ' + os.getcwd() + '/tmp/sandbox/lib/pkgconfig/ to PKG_CONFIG_PATH')
    pkgCfg = subprocess.Popen('export PKG_CONFIG_PATH=' + os.getcwd() + '/tmp/sandbox/lib/pkgconfig/',shell=True,stdout=None)
    pkgCfg.wait()
    
    b = builder()
    b.make(Folder,Configuration,Name)
    
    '''
    
