import unittest
import mox
import os


import urllib

from core.exceptions import LocationNonExistant
import plugins.sys.downloader as download

def md5(filename, against):
    import hashlib
    m = hashlib.md5()
    try:
        fd = open(filename,"rb")
    except IOError:
        print "Unable to open the file in readmode:", filename
        return
    
    content = fd.readlines()
    fd.close()
    for eachLine in content:
        m.update(eachLine)
    digest = m.hexdigest()
    if against == digest:
        return True
    else:
        return digest

def fakehook(nb, bs, fs, url, pbar):
    pass



class TestSysDownloader(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_1_http(self):
        link = 'http://superb-west.dl.sourceforge.net/sourceforge/xine/xine-lib-1.1.16.tar.bz2'
        hashstring = ''
        filename = 'xine-lib-1.1.16.tar.bz2'
        location = os.getcwd() + '/'

        self.mox.StubOutWithMock(urllib, 'urlretrieve', True)
        urllib.urlretrieve('http://superb-west.dl.sourceforge.net/sourceforge/xine/xine-lib-1.1.16.tar.bz2', os.getcwd() + '/xine-lib-1.1.16.tar.bz2')

        self.mox.StubOutWithMock(urllib, 'urlcleanup')
        urllib.urlcleanup()
        
        self.mox.ReplayAll()
        download.http_download(link, location)
        #md5(filename, hashstring)
        self.mox.VerifyAll()

    def test_2_http(self):
        link = 'http://superb-west.dl.sourceforge.net/sourceforge/xine/xine-lib-1.1.16.tar.bz2'
        hashstring = ''
        filename = 'xine-lib-1.1.16.tar.bz2'
        location = 'non-existant'
        self.failUnlessRaises(LocationNonExistant, download.http_download, link, location)

        #md5(filename, hashstring)


    def test_3_ftp(self):
        pass
