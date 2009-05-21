import sys
import unittest

sys.path.append('../')
from Core.Debug import _levelToString
class TestCoreDebug(unittest.TestCase):
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
    