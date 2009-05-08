from Core.Configurator import Configurator
class Arguments:
	def __init__(self):
		self.Cfg = Configurator()
		self.Arguments = {}
	
	def addArgument(self,Argument,Variable,Value,HelpString=None):
		if Argument and Variable and Value:
			self.Arguments[Argument] = {}
			self.Arguments[Argument]['name'] = Variable
			self.Arguments[Argument]['value'] = Value
			if HelpString:
				self.Arguments[Argument]['helpstring'] = HelpString
			else:
				self.Arguments[Argument]['helpstring'] = None
		
			return self.Arguments
		else:
			return False

	def countArguments(self,Arguments):
		Arg = 0
		for ArgV in Arguments[1:]:
			Arg += 1
		if Arg == 0:
			return False
		else:
			return Arg
		
	def parseArguments(self,Arguments):
		for Args in Arguments[1:]:		
			for All in self.Arguments:
				if Args == All:
					self.Cfg.PutGlobal(self.Arguments[All]['name'],self.Arguments[All]['value'])

	def generateHelp(self):
		for All in self.Arguments:
			if self.Arguments[All]['helpstring']:
				print "%s	%s [%s=%s]" % (All,self.Arguments[All]['helpstring'],self.Arguments[All]['name'],self.Arguments[All]['value'])

	
