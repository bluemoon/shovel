import unittest
import mox
import sys

sys.path.append('../')
import core.shovel

class testCoreShovel(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        
        
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
        

    def test_2_main(self):
        shovel = core.shovel.shovel()
        self.mock.StubOutWithMock(shovel, 'arguments')
        shovel.arguments().AndReturn('')   
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
            
