import unittest
import os
import mox
import subprocess
import core.file as file
import plugins.rcs.svn as svn
import plugins

class TestRcsSVN(unittest.TestCase):
    def setUp(self):
        self.svn = svn.cl_svn()
        self.mox = mox.Mox()

    def test_1_checkout(self):
        sourceHttp = "http://finchbot.googlecode.com/svn/trunk/"
        location = 'finch'
        
        #fudge.patch_object(svn.cl_svn.p, 'stdout', '')
        #self.mox.StubOutWithMock(subprocess, 'Popen', True)
        #stdout = self.mox.MockObject()
        #subprocess.Popen = self.mox.StubOutWithMock(subprocess.Popen, '__init__')
        #subprocess.Popen = self.mox.StubOutWithMock(subprocess.Popen, 'stdout')

        #subprocess.Popen('/usr/bin/env svn co\
# http://finchbot.googlecode.com/svn/trunk/ finch', shell=True, stdout=-1).AndReturn(subprocess.Popen.stdout)   
        #self.mox.StubOutWithMock(self.svn.p, 'stdout', True)
        #self.svn.p.stdout = ''
        #self.mox.ReplayAll()
        
        #self.mox.StubOutWithMock()
        #self.svn.checkout(sourceHttp, location)
        #assert os.path.exists(location)
        #self.mock.VerifyAll()
        #subprocess.Popen('rm -rf %s' % (location), shell=True)
        #p.wait()
        
