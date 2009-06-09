import sys
import unittest
import re
import subprocess
import os
import StringIO

sys.path.append('../')
sys.path.append('Plugins/')


import core.shovel

class TestShovel(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.old_value_of_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        self.old_value_of_argv = sys.argv

        #self.cmd.options('../')
    def tearDown(self):
        sys.stdout = self.old_value_of_stdout
        sys.argv = self.old_value_of_argv

    def test_1(self):
        sys.argv = ['--dirt=resources/dirt2']
        m = core.shovel.shovel()
        m.main()
        self.assertStdoutEquals('')
        

