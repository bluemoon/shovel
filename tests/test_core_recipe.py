import unittest
import mox
from core.recipe import *

class testCoreRecipe(unittest.TestCase):
    """docstring for testCoreRecipe"""
    def setUp(self):
        self.mock = mox.Mox()
        self.r = recipe()
        
    def tearDown(self):
        self.mock.UnsetStubs()
        
	def test_1_runner(self):
		self.mock.StubOutWithMock(self.r , 'run')
		self.r.run(mox.IsA(str), mox.IsA(str)).AndReturn(None)
        global feature
        feature = True
        
        self.mock.StubOutWithMock(self.r.config, 'getFeature')     
        self.r.config.getFeature('shovel.sys.downloader').InAnyOrder().AndReturn(feature)
        self.r.config.getFeature('shovel.sys.builder').InAnyOrder().AndReturn(feature)
        self.mock.ReplayAll()


        try:
            self.r.runner('cbuilder')
        except SystemExit, e:
            self.fail(e)
		
        self.mock.VerifyAll()
        
    def test_2_runner(self):
        #self.mock.StubOutWithMock(self.r, 'run')
        #self.r.run(mox.IsA(str), mox.IsA(str)).AndReturn(None)
        #self.mock.ReplayAll()

        self.assertRaises(ImportError,self.r.runner,'idontexist')
        #self.mock.VerifyAll()
