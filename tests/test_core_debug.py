import sys
import unittest
import mox
sys.path.append('../')
from core.debug import _levelToString, _dPrint
from core.debug import *
import core.debug
from core.configurator import configurator
import inspect


class TestCoreDebug(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        
    def tearDown(self):
        self.mock.UnsetStubs()
        
        
    def test_1_L0_levelToString(self):
        assert _levelToString(0) == 'NONE'
    def test_1_L1_levelToString(self):
        assert _levelToString(1) == 'WARNING'
    def test_1_L2_levelToString(self):
        assert _levelToString(2) == 'INFO'
    def test_1_L3_levelToString(self):
        assert _levelToString(3) == 'DEBUG'
    def test_1_Lneg1_levelToString(self):
        assert _levelToString(-1) == 'ERROR'

    def test_2_debug(self):
        self.mock.StubOutWithMock(inspect, 'currentframe')
        inspect.currentframe(0).AndReturn('')  

        self.mock.StubOutWithMock(inspect, 'getouterframes')
        inspect.getouterframes('').AndReturn('')

        #configurator = self.mock.CreateMockAnything()
        #configurator.getGlobal('debug').AndReturn(3)
        #self.mock.StubOutWithMock(core.debug, '_dPrint')
        #debug._dPrint('').AndReturn('')

        self.mock.ReplayAll()

        debug('debug test', DEBUG)

        #self.assertStdoutEquals('')
        self.mock.VerifyAll()

        
    
