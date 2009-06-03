import unittest
import sys
sys.path.append('../')

import core.utils as util
import core.configurator

class TestCoreUtils(unittest.TestCase):
    def setUp(self):
        self.conf = Core.Configurator.Configurator()
    
