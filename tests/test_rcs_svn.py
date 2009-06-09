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
    def tearDown(self):
        self.mox.UnsetStubs()

    def test_1_checkout(self):
        sourceHttp = "http://finchbot.googlecode.com/svn/trunk/"
        location = 'finch'
        

        self.mox.StubOutWithMock(subprocess, 'Popen', True)#, True)

        subprocess.Popen('/usr/bin/env svn co ' +
        'http://finchbot.googlecode.com/svn/trunk/ finch',
        shell=True, stdout=-1).AndReturn(subprocess.Popen)   

        subprocess.Popen.communicate().AndReturn(['',''])     

        self.mox.ReplayAll()
        

        self.svn.checkout(sourceHttp, location)
        self.mox.VerifyAll()
        
