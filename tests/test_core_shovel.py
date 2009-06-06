import unittest
import mox
import sys
sys.path.append('../')
import core.shovel

class testCoreShovel(object):
    def setUp(self):
        self.mock = mox.Mox()
        
        
    def test_1_arguments(self):
        shovel = core.shovel.shovel()
        self.mock.StubOutWithMock(shovel, 'parseOptions')
        shovel.parseOptions().AndReturn('')
        
    def test_2_main(self):
        shovel = core.shovel.shovel()
        self.mock.StubOutWithMock(shovel, 'arguments')
        shovel.arguments().AndReturn('')
        self.mock.ReplayAll()
        shovel.main()
