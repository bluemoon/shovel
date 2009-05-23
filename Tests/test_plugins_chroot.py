import unittest
import sys
sys.path.append('../')

from Plugins.chroot import chroot
class TestPluginsChroot(unittest.TestCase):
    def test_1_chroot(self):
        c = chroot()
        #c.init('tmp/chroot')

