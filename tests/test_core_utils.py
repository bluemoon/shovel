import unittest
import sys
sys.path.append('../')

import Core.Utils as util
import Core.Configurator

class TestCoreUtils(unittest.TestCase):
    def setUp(self):
        self.conf = Core.Configurator.Configurator()
    