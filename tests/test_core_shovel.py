import unittest
import mox
import sys

sys.path.append('../')
import core.shovel

class testCoreShovel(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()
    def tearDown(self):
        self.mock.UnsetStubs()  
        
    def test_1_argument(self):
        shovel = core.shovel.shovel()
        #self.mock.StubOutWithMock(shovel, 'parseOptions')
        #shovel.parseOptions().AndReturn('')
        options = {'tests': None, 'nonpretty': None, 'verbose': None, 
        'dirt': None, 'lexer': None, 'recipe': None, 'verbose_single': None, 
        'sandbox': None, 'clean': None, 'config': None}
        
        #self.mock.StubOutWithMock(shovel, 'parseOptions')
        #shovel.parseOptions().AndReturn('')
        #self.mock.StubOutWithMock(shovel, 'parse_args')
        #shovel.parse_args().AndReturn
        #shovel.options = mox.MockObject(options)
        
        #self.mock.ReplayAll()
        #shovel.arguments()
        #self.mock.VerifyAll()
        
    def setupMain(self):
        self.mock.StubOutWithMock(self.shovel, 'arguments')
        self.shovel.arguments().AndReturn('')   

        self.mock.StubOutWithMock(self.shovel.plugins, 'getAll')
        self.shovel.plugins.getAll()
        
        self.mock.StubOutWithMock(self.shovel.config, 'getGlobal')
        self.shovel.config.getGlobal('dirt').InAnyOrder()
        self.shovel.config.getGlobal('lexer').InAnyOrder()
        self.shovel.config.getGlobal('tests').InAnyOrder()

    def test_2_main(self):
        self.shovel = core.shovel.shovel()
        self.setupMain()

        self.mock.ReplayAll()
        
        try:
            self.shovel.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
        except Exception, e:
            self.fail('unexpected exception: %s' % e)
        else:
            self.fail('SystemExit exception expected')
            
            
        self.mock.VerifyAll()

    def test_3_main(self):
        shovel = core.shovel.shovel()
        self.mock.StubOutWithMock(shovel, 'arguments')
        shovel.arguments().AndReturn('')   

        self.mock.StubOutWithMock(shovel.plugins, 'getAll')
        shovel.plugins.getAll()
        
        self.mock.StubOutWithMock(shovel.config, 'getGlobal')
        shovel.config.getGlobal('dirt').InAnyOrder().AndReturn(None)
        shovel.config.getGlobal('lexer').InAnyOrder().AndReturn('yaml')
        shovel.config.getGlobal('tests').InAnyOrder().AndReturn(None)

        self.mock.StubOutWithMock(shovel.yml, 'load')
        shovel.yml.load('None')
        self.mock.StubOutWithMock(shovel.yml, 'run')
        shovel.yml.run()

        self.mock.ReplayAll()
        
        try:
            shovel.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
        except Exception, e:
            self.fail('unexpected exception: %s' % e)
        else:
            self.fail('SystemExit exception expected')
            
            
        self.mock.VerifyAll()      
    def test_4_main(self):
        shovel = core.shovel.shovel()
        self.mock.StubOutWithMock(shovel, 'arguments')
        shovel.arguments().AndReturn('')   

        self.mock.StubOutWithMock(shovel.plugins, 'getAll')
        shovel.plugins.getAll()
        
        self.mock.StubOutWithMock(shovel.config, 'getGlobal')
        shovel.config.getGlobal('dirt').InAnyOrder().AndReturn('resources/dirt2')
        shovel.config.getGlobal('lexer').InAnyOrder().AndReturn('yaml')
        shovel.config.getGlobal('tests').InAnyOrder().AndReturn(None)

        self.mock.StubOutWithMock(shovel.yml, 'load')
        shovel.yml.load('resources/dirt2')
        self.mock.StubOutWithMock(shovel.yml, 'run')
        shovel.yml.run()

        self.mock.ReplayAll()
        
        try:
            shovel.main()
        except SystemExit, e:
            self.assertEquals(type(e), type(SystemExit()))
        except Exception, e:
            self.fail('unexpected exception: %s' % e)
        else:
            self.fail('SystemExit exception expected')
            
            
        self.mock.VerifyAll()
