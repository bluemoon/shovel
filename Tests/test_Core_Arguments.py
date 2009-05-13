import libpry
import sys
sys.path.append('../')
sys.path.append('Plugins/')
class TestCoreArguments(libpry.AutoTree):
  def setUpAll(self):
    sys.path.append('../')
    from Core.Arguments import Arguments
    self.Arg = Arguments()
  def test_1_addArgument(self):
	  assert self.Arg.addArgument('--np','nonpretty',True) == {'--np': {'helpstring': None, 'name': 'nonpretty', 'value': True}}
  def test_2_addArgument_w_HelpString(self):
    assert self.Arg.addArgument('--np3','nonpretty',True,'Takes all the formatting out') == {'--np': {'helpstring': None, 'name': 'nonpretty', 'value': True}, '--np3': {'helpstring': 'Takes all the formatting out', 'name': 'nonpretty', 'value': True}} 
  def test_3_countArguments(self):
    assert self.Arg.countArguments(['setup.py','--np']) == 1
  def test_4_False_countArguments(self):
    assert self.Arg.countArguments(['setup.py']) == False
	# XXX: Add def parseArguments(self,Arguments)
tests = [
  TestCoreArguments()
]
