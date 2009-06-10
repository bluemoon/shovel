import unittest
import mox

import parsers.nyaml as nyaml
import os
import sys
import yaml
import inspect

import core.debug

class testParsersNyaml(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_1_fail_load(self):
        yml = nyaml.nyaml()        
        
        self.mox.StubOutWithMock(os.path, 'exists')
        os.path.exists('dirt').AndReturn(False)

        self.mox.StubOutWithMock(sys, 'exit')
        sys.exit(-1)

        self.mox.ReplayAll()
        yml.load('dirt')
        self.mox.VerifyAll()

    def test_2_load(self):
        yml = nyaml.nyaml()        
        
        self.mox.StubOutWithMock(os.path, 'exists')
        os.path.exists('tests/test_nyaml_dirt2').AndReturn(True)

        self.mox.StubOutWithMock(yaml, 'load')
        yaml.load(mox.IgnoreArg())

        self.mox.ReplayAll()
        yml.load('tests/test_nyaml_dirt2')
        self.mox.VerifyAll()

    def test_3_run(self):
        cwd = os.getcwd()


        dyaml = {'commit': {'test_directory': 'tests',
        'recipe': 'test -> commit', 'test_command': 'nosetests'}, 
        'pre.flight': {'ffmpeg': {'recipe': 'cbuilder', 
        'link': 'http://ffmpeg.mplayerhq.hu/releases/ffmpeg-0.5.tar.bz2', 
        'configure': ['--enable-postproc --enable-gpl --disable-mmx --disable-mmx2'],
        'md5': 'be8503f15c3b81ba00eb8379ca8dcf33'}, 'xine': {'recipe': 'cbuilder',
        'link': 'http://superb-west.dl.sourceforge.net/sourceforge/xine/xine-lib-1.1.16.tar.bz2',
        'md5': 'acd1a210c5a6444e8fd44696469352bb'}}}
        
        yml = nyaml.nyaml()
        
        #self.mox.StubOutWithMock(os.path, 'exists')
        #os.path.exists('resources/dirt2').AndReturn(True)
        #os.path.exists(mox.IsA(str))

        
        

        self.mox.StubOutWithMock(yaml, 'load')
        yaml.load(mox.IgnoreArg()).AndReturn(dyaml)

        self.mox.StubOutWithMock(yml.recipe, 'runner')
        yml.recipe.runner(mox.IsA(str), mox.IsA(list))
        yml.recipe.runner(mox.IsA(str), mox.IsA(list))
        yml.recipe.runner(mox.IsA(str), mox.IsA(list))
        yml.recipe.runner(mox.IsA(str), mox.IsA(list))
        #self.mox.StubOutWithMock(inspect, 'currentframe')
        #inspect.currentframe(mox.IgnoreArg())

        #self.mox.StubOutWithMock(inspect, 'getouterframes')
        #inspect.getouterframes(mox.IgnoreArg())

        self.mox.ReplayAll()

        yml.load('tests/test_nyaml_dirt2')
        yml.run()

        self.mox.VerifyAll()
