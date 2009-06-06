import unittest
import os
import core.file as f

class TestCoreFile(unittest.TestCase):
    def test_1_touch(self):
        f.touch('test_touch')
        exists = os.path.exists('test_touch')
        assert exists == True
        os.remove('test_touch')
        
    def test_2_chdir(self):
        cwd = os.getcwd()
        f.chdir('tests')
        nCwd = os.getcwd()
        assert nCwd == cwd + '/tests'
        f.chdir(cwd)
        
    def test_3_fail_condChroot(self):
        self.assertRaises(NameError, f.condChroot,'blah')
        
    def test_4_mkdirIfAbsent(self):
        f.mkdirIfAbsent('test')
        exists = os.path.exists('test')    
        assert exists == True
        os.removedirs('test')
        
        
    def test_5_rmDirectoryRecursive(self):
        ## Create a bunch of directories to recursively delete
        f.mkdirIfAbsent('test')
        f.mkdirIfAbsent('test/me')
        f.mkdirIfAbsent('test/me/lots')
        f.mkdirIfAbsent('test/me/lots/of')
        f.mkdirIfAbsent('test/me/lots/of/times')
        
        f.rmDirectoryRecursive('test')
        exists = os.path.exists('test')
        assert exists == False  
        
    def test_6_single_rmDirectoryRecursive(self):
        f.mkdirIfAbsent('test')
        f.rmDirectoryRecursive('test')
        exists = os.path.exists('test')
        assert exists == False  
