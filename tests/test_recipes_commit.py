import unittest
import mox

import os
import recipes.commit

class TestRecipesCommit(unittest.TestCase):
    def setUp(self):
        self.mox =  mox.Mox()
    def tearDown(self):
        self.mox.UnsetStubs() 

    def test_1_whatRcsType(self):
        self.mox.StubOutWithMock(os, 'getcwd')
        os.getcwd().AndReturn('')

        self.mox.StubOutWithMock(os, 'chdir')
        os.chdir('/home').InAnyOrder('chdir')
        os.chdir('').InAnyOrder('chdir')

        self.mox.StubOutWithMock(os.path, 'exists')
        os.path.exists('.git').InAnyOrder('exists').AndReturn(True)
        #os.path.exists('.svn').InAnyOrder('exists').AndReturn(False)
        
        self.mox.ReplayAll()
        rcsType = recipes.commit.whatRcsType('/home')
        assert rcsType == 'git'
        self.mox.VerifyAll()

    def test_2_whatRcsType(self):
        self.mox.StubOutWithMock(os, 'getcwd')
        os.getcwd().AndReturn('')

        self.mox.StubOutWithMock(os, 'chdir')
        os.chdir('/home').InAnyOrder('chdir')
        os.chdir('').InAnyOrder('chdir')

        self.mox.StubOutWithMock(os.path, 'exists')
        os.path.exists('.git').InAnyOrder('exists').AndReturn(False)
        os.path.exists('.svn').InAnyOrder('exists').AndReturn(False)
        
        self.mox.ReplayAll()
        rcsType = recipes.commit.whatRcsType('/home')
        assert rcsType == None
        self.mox.VerifyAll()
