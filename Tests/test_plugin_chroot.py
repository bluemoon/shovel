import sys
sys.path.append('../')

from Plugins.chroot import chroot

c = chroot()
c.init('tmp/chroot')
