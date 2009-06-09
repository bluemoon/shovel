import sys
import unittest

sys.path.append('../')
from core.debug import _levelToString
from core.debug import *
import StringIO

class TestCoreDebug(unittest.TestCase):
    def setUp(self):
        self.old_value_of_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        
    def tearDown(self):
        sys.stdout = self.old_value_of_stdout
        
        
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
        debug('debug test', DEBUG)
        self.assertEquals('',sys.stdout.getvalue())
        #self.assertStdoutEquals('')


        
    
