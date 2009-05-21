import unittest

import Core.Utils as util
import Core.Configurator

class TestCoreUtils(unittest.TestCase):
    def setUp(self):
        self.conf = Core.Configurator.Configurator()
    