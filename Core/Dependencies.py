class Dependencies:
	def __init__(self):
		self.DependencyList = {}
	def BuildCoreDependencies(self,CoreDep):
		self.DependencyList = CoreDep
	def DependencyGeneratorAdd(self,Dependant,DependsOn=None):
		if DependsOn == None:
			self.DependencyList[Dependant] = []
		else:
			self.DependencyList[Dependant] = []
			self.DependencyList[Dependant].append(DependsOn)
	def DependencyGeneratorRun(self):
		D = dict((k, set(self.DependencyList[k])) for k in self.DependencyList)
		R = []
		while D:
			t = set(i for v in D.values() for i in v)-set(D.keys())
			t.update(k for k, v in D.items() if not v)
			R.append(t)
			D = dict(((k, v-t) for k, v in D.items() if v))
			return R