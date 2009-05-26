## Core imports
from Core.Blocks        import Blocks
from Core.Dependencies  import Dependencies
from Core.Configurator  import Configurator
from Core.Features      import Features
from Core.Exceptions    import ParseError, DirtFileDoesntExist
from Core.Debug         import *
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
        
    def dirtExists(self,File):
	""" Check to see if the dirt file exists"""
        if os.path.exists(File):
            return True
        else:
            return False
    
    def loadDirt(self,File):
        """ Load the dirt File """
        if self.dirtExists(File):
            dirtFile = open(File, 'r')
            dFile = dirtFile.read()
            self.dirtY = yaml.load(dFile,Loader=Loader)
        else:
            raise DirtFileDoesntExist
    
    def main(self,fileName,remainder):
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
            self.run(All=True)
            
        ## Otherwise run the specified block    
        else:
            for remain in remainder:
                self.run(remain)
    
    def run(self,All=False):
        ''' this is the main runner for the yaml parser '''
        ## Run all of the blocks
        if All:
            for cmds in self.commands:
                self.runBlock(cmds)
                self.depRunner(cmds)
                
        ## If value hasnt changed, raise ParseError
		if not All:
		    raise ParseError
        ## Otherwise run specified block
        else:         
            self.runBlock(All)
            self.depRunner(All)
                
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
            
    def workRunner(self,Block,Work):
        debug("block: "+Block + " work: " +Work,DEBUG)
        for work in self.dirtY[self.os[0]][Block][Work]:
            if hasattr(work,'keys'):
                for Keys in work.keys():
                    if hasattr(work[Keys],'keys'):
                        if work[Keys].has_key('use'):
                            if self.config.getFeature(work[Keys]['use']):
                                self.config.PutPackage(Work,self.dirtY[self.os[0]][Block][Work])
                                self.features.RunFeature(work[Keys],Work)
                            else:
                                debug("Not loaded: "+work[Keys]['use'],ERROR)
                    else:
                        raise ParseError
            else:
                raise ParseError
				
    def depRunner(self,Block):
        for runner in self.dirtY[self.os[0]][Block]:
            if hasattr(self.dirtY[self.os[0]][Block][runner],'keys'):
                raise ParseError
            else:
                for lst in self.dirtY[self.os[0]][Block][runner]:
                    if hasattr(lst,'keys'):
                        if lst.has_key('dependencies'):
                            if hasattr(lst['dependencies'],'keys'):
                                if lst['dependencies'].has_key('use'):
                                    pass
                            else:
                                for Deps in lst['dependencies']:
                                    debug("[" +runner + "] depends on: " + Deps, INFO)
                                    self.deps.DependencyGeneratorAdd(runner,Deps)
                        else:
                            self.deps.DependencyGeneratorAdd(runner)
                    else:
                        raise ParseError
						
        DepList = self.deps.dependencyGenRun()
        Rev = []
        for RevDep in DepList[0]:
            Rev.append(RevDep)
			
        while Rev:
            Work = Rev.pop()
            self.workRunner(Block,Work)
			
    def runFeatureBlock(self,Block):
        Counter = 0
        for Runner in self.Blocks.ParseBlock(self.dirtY[Block],True):
            debug(Runner, DEBUG)
            List = self.dirtY[Block][Runner]
            List.reverse()
            print List.pop()
            for subRunner in self.dirtY[Block][Runner]:
                for mF in self.blocks.ParseBlock(subRunner):
                    if hasattr(subRunner[mF],'keys'):
                        if subRunner[mF].has_key('use'):
                            print subRunner[mF]['use']
                            Feature = self.config.getFeature(subRunner[mF]['use'])
                            if Feature:
                                self.features.RunFeature(subRunner[mF],subRunner)
                    if subRunner.has_key('use'):
                        print subRunner['use']

	
    def runBlock(self,Block):
        for Runner in self.blocks.ParseBlock(self.dirtY[self.os[0]][Block]):
            sub = self.blocks.ParseBlock(self.dirtY[self.os[0]][Block][Runner])
            for SubRunner in sub:
                if SubRunner == 'use':
                    Name = self.features.SplitClass(self.dirtY[self.os[0]][Block][Runner][SubRunner])
                    Feature = self.config.getFeature(self.dirtY[self.os[0]][Block][Runner][SubRunner])
                    if not Feature: 
                        debug("Feature " +TermOrange + self.dirtY[Block][Runner][SubRunner] + TermEnd + " is not available", WARNING)
                    else:
                        debug("Instance created: "+ TermGreen + self.dirtY[Block][Runner][SubRunner] + TermEnd, INFO)
                for uberSubRunner in self.blocks.ParseBlock(self.dirtY[self.os[0]][Block][Runner][SubRunner]):
                    if uberSubRunner == 'use':
                        Name = self.features.SplitClass(self.dirtY[self.os[0]][Block][Runner][SubRunner][uberSubRunner])
                        Feature = self.config.getFeature(self.dirtY[self.os[0]][Block][Runner][SubRunner]['use'])
                        if not Feature:
                            debug("Feature "+ TermOrange+ self.dirtY[self.os[0]][Block][Runner][SubRunner][uberSubRunner]+TermEnd + " is not available", WARNING)
                        else:
                            debug("Instance created: "+ TermGreen + self.dirtY[self.os[0]][Block][Runner][SubRunner][uberSubRunner] + TermEnd, INFO)
                    else:
                        pass
                        
