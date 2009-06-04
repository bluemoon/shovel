## File: dependencies.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)


class dependencies:
    def __init__(self):
        self.depList = {}
        
    def buildCoreDeps(self, coreDep):
        self.depList = coreDep

    def depGenAdd(self, dependant, dependsOn=None):
        if dependsOn == None:
            self.depList[dependant] = []
        else:
            self.depList[dependant] = []
            self.depList[dependant].append(dependsOn)

    def dependencyGenRun(self):
        lstDict = dict((k, set(self.depList[k])) for k in self.depList)
        R = []
        while lstDict:
            t = set(i for v in lstDict.values() for i in v)-set(lstDict.keys())
            t.update(k for k, v in lstDict.items() if not v)
            R.append(t)
            lstDict = dict(((k, v-t) for k, v in lstDict.items() if v))
        return R
