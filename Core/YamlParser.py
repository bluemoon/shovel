## Core imports
from Core.Blocks        import Blocks
from Core.Dependencies  import Dependencies
from Core.Configurator  import Configurator
from Core.Features      import Features
from Core.Exceptions    import ParseError, DirtFileDoesntExist
from Core.Debug         import *
from Core.Terminal      import TermOrange
from Core.Terminal      import TermEnd
from Core.Terminal      import TermGreen
## System imports
import os
import yaml

from yaml import load, dump

try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class yamlParser(object):
    def __init__(self):
        self.commands = []
        self.os       = os.uname()
        
        self.blocks   = Blocks()
        self.deps     = Dependencies()
        self.config   = Configurator()
        self.features = Features()
        
    def dirtExists(self, file):
	""" Check to see if the dirt file exists"""
        if os.path.exists(file):
            return True
        else:
            return False
    
    def loadDirt(self, file):
        """ Load the dirt file """
        if self.dirtExists(file):
            dirtFile = open(file, 'r')
            dFile = dirtFile.read()
            self.dirtY = yaml.load(dFile,Loader=Loader)
        else:
            raise DirtFileDoesntExist
    
    def main(self, fileName, remainder):
        ''' the main code for the yaml parser '''
        self.loadDirt(fileName)
        
        ## Check to see if the dirt file has the right OS
        Os = self.getOs()
        
        ## Turn all of the blocks into commands ie. pre.flight build etc.
        self.commands = self.getCommands()
        
        ## Compare those to whats leftover from optparse
        remain = self.argumentRemainders(remainder)
        
        self.getAllUse()
        ## If not, run all the blocks
        if not remain:
            self.run(all=True)
            
        ## Otherwise run the specified block    
        else:
            for remain in remainder:
                self.run(remain)
    
    def run(self, all=False):
        ''' this is the main runner for the yaml parser '''
        ## Run all of the blocks
        if all:
            for cmds in self.commands:
                self.runBlock(cmds)
                self.depRunner(cmds)
                
        ## If value hasnt changed, raise ParseError
		if not all:
		    raise ParseError
        ## Otherwise run specified block
        else:         
            self.runBlock(all)
            self.depRunner(all)
                
    def getOs(self):
        osBlock = self.parseOsBlock()
        if self.blockOSspecific(osBlock):
            ## returns the block if it matches the OS
            return osBlock
        else:
            ## otherwise fail!
            return False
        
    def getCommands(self):
        ## Get all of the commands from the dirt file
        self.commands = self.blocks.ParseBlock(self.dirtY[self.os[0]])
        return self.commands
        
    def parseOsBlock(self):
        osBlock = self.blocks.ParseBlock(self.dirtY)
        return osBlock
        
    def blockOSspecific(self,Block):
        for os in Block:
            if os == self.os[0]:
                return True
                
    def commandOutOfBlock(self,Block):
		for B in Block:
			self.commands.append(B)
			
    def argumentRemainders(self,remainder):
        for remainders in remainder:
            if remainders in self.commands:
                return True
                
    def getAllUse(self):
        def use(x): return x == 'use'
        for a in self.dirtY[self.os[0]]:
            #print map(use,a) 		
            pass
            
    def workRunner(self, block, work):
        debug("block: "+block + " work: " +work,DEBUG)
        for work in self.dirtY[self.os[0]][block][work]:
            if hasattr(work,'keys'):
                for keys in work.keys():
                    if hasattr(work[keys],'keys'):
                        if work[keys].has_key('use'):
                            if self.config.getFeature(work[keys]['use']):
                                self.config.PutPackage(work,self.dirtY[self.os[0]][block][work])
                                self.features.RunFeature(work[keys],work)
                            else:
                                debug("Not loaded: "+work[keys]['use'],ERROR)
                    else:
                        raise ParseError
            else:
                raise ParseError
				
    def depRunner(self, block):
        for runner in self.dirtY[self.os[0]][block]:
            if hasattr(self.dirtY[self.os[0]][block][runner],'keys'):
                raise ParseError
            else:
                for lst in self.dirtY[self.os[0]][block][runner]:
                    if hasattr(lst,'keys'):
                        if lst.has_key('dependencies'):
                            if hasattr(lst['dependencies'],'keys'):
                                if lst['dependencies'].has_key('use'):
                                    pass
                            else:
                                for Deps in lst['dependencies']:
                                    debug("[" +runner + "] depends on: " + Deps, INFO)
                                    self.deps.depGenAdd(runner,Deps)
                        else:
                            self.deps.depGenAdd(runner)
                    else:
                        raise ParseError
						
        depList = self.deps.dependencyGenRun()
        rev = []
        for revDep in depList[0]:
            rev.append(revDep)
			
        while rev:
            work = rev.pop()
            self.workRunner(block, work)
			
    def runFeatureBlock(self, block):
        for runner in self.block.ParseBlock(self.dirtY[block],True):

            debug(runner, DEBUG)

            list = self.dirtY[block][runner]
            list.reverse()
            
            for subRunner in self.dirtY[block][runner]:
                for mF in self.blocks.ParseBlock(subRunner):
                    if hasattr(subRunner[mF],'keys'):
                        if subRunner[mF].has_key('use'):
			    feature = self.config.getFeature(subRunner[mF]['use'])
                            if feature:
                                self.features.RunFeature(subRunner[mF],subRunner)
                    if subRunner.has_key('use'):
                        print subRunner['use']

	
    def runBlock(self, block):
        for runner in self.blocks.ParseBlock(self.dirtY[self.os[0]][block]):
            sub = self.blocks.ParseBlock(self.dirtY[self.os[0]][block][runner])
            for subRunner in sub:
                if subRunner == 'use':
		    feature = self.config.getFeature(self.dirtY[self.os[0]][block][runner][subRunner])
                    if not feature: 
                        debug("feature " + TermOrange + self.dirtY[block][runner][subRunner] + TermEnd + " is not available", WARNING)
                    else:
                        debug("Instance created: "+ TermGreen + self.dirtY[block][runner][subRunner] + TermEnd, INFO)
                for uberSubRunner in self.blocks.ParseBlock(self.dirtY[self.os[0]][block][runner][subRunner]):
                    if uberSubRunner == 'use':
                        name = self.features.SplitClass(self.dirtY[self.os[0]][block][runner][subRunner][uberSubRunner])
                        feature = self.config.getFeature(self.dirtY[self.os[0]][block][runner][subRunner]['use'])
                        if not feature:
                            debug("feature "+ TermOrange+ self.dirtY[self.os[0]][block][runner][subRunner][uberSubRunner]+TermEnd + " is not available", WARNING)
                        else:
			    
                            debug("Instance created: "+ TermGreen + self.dirtY[self.os[0]][block][runner][subRunner][uberSubRunner] + TermEnd, INFO)
                    else:
                        pass
                        
