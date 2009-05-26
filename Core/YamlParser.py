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


class yamlParser(object):
    ''' the main yaml parser '''
    def __init__(self):
        self.commands = []
        self._os      = os.uname()
        self.blocks   = Blocks()
        self.deps     = Dependencies()
        self.config   = Configurator()
        self.features = Features()
        
    def dirtExists(self, fileName):
        """ Check to see if the dirt file exists"""
        if os.path.exists(fileName):
            return True
        else:
            return False
    
    def loadDirt(self, fileName):
        """ Load the dirt fileName """
        if self.dirtExists(fileName):
            dirtFile = open(fileName, 'r')
            dFile = dirtFile.read()
            self.dirtY = yaml.load(dFile)
        else:
            raise DirtFileDoesntExist
    
    def main(self, fileName, remainder):
        ''' the main code for the yaml parser '''
        self.loadDirt(fileName)
        
        ## Check to see if the dirt file has the right OS
        _os = self.getOs()
        
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
    
    def run(self, _all=False):
        ''' this is the main runner for the yaml parser '''
        ## Run all of the blocks
        if _all:
            for cmds in self.commands:
                self.runBlock(cmds)
                self.depRunner(cmds)

        ## If value hasnt changed, raise ParseError
        if not _all:
            raise ParseError
        ## Otherwise run specified block
        else:
            self.runBlock(_all)
            self.depRunner(_all)
                
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
        self.commands = self.blocks.ParseBlock(self.dirtY[self._os[0]])
        return self.commands
        
    def parseOsBlock(self):
        osBlock = self.blocks.ParseBlock(self.dirtY)
        return osBlock
        
    def blockOSspecific(self, block):
        for t_os in block:
            if t_os == self._os[0]:
                return True
                
    def commandOutOfBlock(self, block):
        ''' make a command out of the block '''
        for all_b in block:
            self.commands.append(all_b)
                        
    def argumentRemainders(self, remainder):
        ''' handles anything thats left over '''
        for remainders in remainder:
            if remainders in self.commands:
                return True
                
    def getAllUse(self):
        for _all in self.dirtY[self._os[0]]:
            print _all
            
    def workRunner(self, block, work):
        ''' actually runs the work '''
        debug("block: "+block + " work: " +work, DEBUG)
        for work in self.dirtY[self._os[0]][block][work]:
            if hasattr(work, 'keys'):
                for keys in work.keys():
                    if hasattr(work[keys], 'keys'):
                        if work[keys].has_key('use'):
                            if self.config.getFeature(work[keys]['use']):
                                package = self.dirtY[self._os[0]][block][work]
                                self.config.PutPackage(work, package)
                                self.features.RunFeature(work[keys], work)
                            else:
                                debug("Not loaded: "+work[keys]['use'], ERROR)
                    else:
                        raise ParseError
            else:
                raise ParseError
				
    def depRunner(self, block):
        ''' resolves the dependencies '''
        for runner in self.dirtY[self._os[0]][block]:
            if hasattr(self.dirtY[self._os[0]][block][runner], 'keys'):
                raise ParseError
            else:
                for lst in self.dirtY[self._os[0]][block][runner]:
                    if hasattr(lst, 'keys'):
                        if lst.has_key('dependencies'):
                            if hasattr(lst['dependencies'], 'keys'):
                                if lst['dependencies'].has_key('use'):
                                    pass
                            else:
                                for deps in lst['dependencies']:
                                    debug("[" +runner + "] depends on: " + deps, INFO)
                                    self.deps.depGenAdd(runner, deps)
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
        ''' run a feature block '''
        for runner in self.blocks.ParseBlock(self.dirtY[block], True):

            debug(runner, DEBUG)

            lst = self.dirtY[block][runner]
            lst.reverse()
            
            for subRunner in self.dirtY[block][runner]:
                for m_F in self.blocks.ParseBlock(subRunner):
                    if hasattr(subRunner[m_F], 'keys'):
                        if subRunner[m_F].has_key('use'):
                            feature = self.config.getFeature(subRunner[m_F]['use'])
                            if feature:
                                self.features.RunFeature(subRunner[m_F], subRunner)
                    if subRunner.has_key('use'):
                        print subRunner['use']

	
    def runBlock(self, block):
        ''' run the block of code '''
        for runner in self.blocks.ParseBlock(self.dirtY[self._os[0]][block]):
            sub = self.blocks.ParseBlock(self.dirtY[self._os[0]][block][runner])
            for subRunner in sub:
                if subRunner == 'use':
                    featureName = self.dirtY[self._os[0]][block][runner][subRunner]
                    feature = self.config.getFeature(featureName)
                    if not feature:
                        debug("feature " + TermOrange + featureName \
                              + TermEnd + " is not available", WARNING)
                    else:
                        debug("Instance created: "+ TermGreen + \
                              self.dirtY[block][runner][subRunner] + \
                              TermEnd, INFO)
                b_R = self.dirtY[self._os[0]][block][runner][subRunner]
                for uberSubRunner in self.blocks.ParseBlock(b_R):
                    if uberSubRunner == 'use':
                        feature = self.config.getFeature(self.dirtY[self._os[0]][block][runner][subRunner]['use'])
                        if not feature:
                            debug("feature "+ TermOrange + \
                                  self.dirtY[self._os[0]][block][runner][subRunner][uberSubRunner]+ \
                                  TermEnd + " is not available", WARNING)
                        else:
			    
                            debug("Instance created: " + TermGreen +\
                                  self.dirtY[self._os[0]][block][runner][subRunner][uberSubRunner] +\
                                  TermEnd, INFO)
                    else:
                        pass
                        
