import sys
import unittest
import re
import subprocess
import os

sys.path.append('../')
sys.path.append('Plugins/')



class CommandLine(object):
    def __init__(self):
        self.directory = None
        self.cwd = os.getcwd()
        
    def options(self, directory=None):
        if directory:
            self.directory = directory
            
    def run(self, program, options, error):
        if self.directory:
            os.chdir(self.directory)
            
        erRegex = re.compile(error)
        programProcess = subprocess.Popen(program + ' ' + options, 
        shell=True, stdout=subprocess.PIPE)

        stdout = programProcess.communicate()
        for output in stdout:
            if erRegex.match(output):
                return False
                break
                    
        if self.directory:
            os.chdir(self.cwd)
        

class TestShovel(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.cmd = CommandLine()
        #self.cmd.options('../')
        
    def test_1(self):
        #out = self.cmd.run(self.cwd + '/shovel','--dirt=non-existant',
        #'Core\.Exceptions\.DirtFileDoesntExist')
        #assert out == False
        pass

