## Core imports
from core.dependencies  import dependencies
from core.configurator  import configurator
from core.features      import Features
from core.exceptions    import ParseError, DirtFileDoesntExist
from core.debug         import *
from core.utils         import TermOrange
from core.utils         import TermEnd
from core.utils         import TermGreen
## System imports
import os
import yaml

def yamlReduce(yaml, lst):
    return reduce(dict.get, lst, yaml)

class yamlGenerators(object):
    def os(self, dictionary):
        for os in dictionary.items():
            yield os
            
    def block(self, dictionary):
        for os, a in dictionary.items():
            for block, b in reversed(a.items()):
                yield {
                'os'    : os,
                'block' : block
                }
                
    def subblock(self, dictionary):
        for os, a in dictionary.items():
            for block, b in a.items():
                for subblock, c in b.items():
                    yield subblock
                    
            
    def feature(self, dictionary):
        for os, a in dictionary.items():
            for block, b in a.items():
                for subblock, c in reversed(b.items()):
                    for feature, d in c[0].items():
                        yield{
                        'os'   : os,
                        'block': block,
                        'subblock': subblock,
                        'feature': feature,
                        }
                        
    def featureBlock(self, dictionary):
        for _os, a in dictionary.items():
            for _block, b in a.items():
                for _subblock, c in reversed(b.items()):
                    for _feature, d in c[0].items():
                        for _fb in d.items(): 
                            yield{
                                'os'      : _os,
                                'block'   : _block,
                                'subblock': _subblock,
                                'feature' : _feature,
                                'fb'      : _fb,
                            }
                            
class yamlParser(object):
    ''' the main yaml parser '''
    def __init__(self):
        self.commands = []
        self._os      = os.uname()
        self.deps     = dependencies()
        self.config   = configurator()
        self.features = features()
        self.gen      = yamlGenerators()
        
        
    
    def loadDirt(self, fileName):
        """ Load the dirt fileName """
        if not os.path.exists(fileName):
            raise DirtFileDoesntExist
        else:
            dirtFile = open(fileName, 'r')
            dFile = dirtFile.read()
            self.dirtY = yaml.load(dFile)
            
                
    
    def main(self, fileName, remainder):
        ''' the main code for the yaml parser '''
        self.loadDirt(fileName)
        
        ## Turn all of the blocks into commands ie. pre.flight build etc.
        self.commands = self.getCommands()
        if not self.commands:
            raise Exception('OSnotFound')
            
        ## Compare those to whats leftover from optparse
        remain = self.argumentRemainders(remainder)
        
        
        ## If not, run all the blocks
        if not remain:
            self.run(_all=True)
            
        ## Otherwise run the specified block    
        else:
            for remain in remainder:
                self.run(remain)
    
    def run(self, _all=False):
        ''' this is the main runner for the yaml parser '''
        ## Run all of the blocks
        if _all:
            for cmds in self.commands:
                debug(cmds, DEBUG)
                self.runBlock(cmds)
                self.depRunner(cmds)

        ## If value hasnt changed, raise ParseError
        if not _all:
            raise ParseError
        ## Otherwise run specified block
        else:
            #debug(_all, DEBUG)
            self.runBlock(_all)
            self.depRunner(_all)
               


        
    def getCommands(self):
        ''' Get all of the commands from the dirt file '''
        self.commands = [x['block'] for x in self.gen.block(self.dirtY) \
        if x['os'] == self._os[0]]
        return self.commands
    
                        
    def argumentRemainders(self, remainder):
        ''' handles anything thats left over '''
        for remainders in remainder:
            if remainders in self.commands:
                return True
                
                
    def featureDebug(self, feature, name):
        if feature:
            debug("instance of " + TermGreen + name \
            + TermEnd + " created!", INFO)
        else:
            debug("feature " + TermOrange + name \
            + TermEnd + " not available.", WARNING)
        
    def runBlock(self, block):
        ''' run the block of code '''
        debug(self._os[0],DEBUG)
        for gen in self.gen.featureBlock(self.dirtY):
            if gen['os'] == self._os[0]:
                if gen['block'] == block and gen['fb'][0] == 'use':
                    feature = self.config.getFeature(gen['fb'][1])
                    self.featureDebug(feature, gen['fb'][1])
            
        #for runner in self.blocks.ParseBlock(self.dirtY[self._os[0]][block]):
        #        self.subRunBlock(block, runner)
                    
    def workRunner(self, block, work):
        debug('block: ' + block + ' work: ' + work)
        # [gen for gen in self.gen.featureBlock(self.dirtY) if gen['']]
        for gen in self.gen.featureBlock(self.dirtY):
            if gen['fb'][0] == 'use' and gen['block'] == block \
            and gen['os'] == self._os[0] and gen['subblock'] == work:
                
                feature = self.config.getFeature(gen['fb'][1])
                if feature:
                    self.config.putPackage(work, gen['feature'])
                    lst = [gen['os'], gen['block'], gen['subblock']]
                    features = yamlReduce(self.dirtY, lst)[0][gen['feature']]
                    self.features.RunFeature(gen['fb'][1], gen['subblock'], features)
   
                else:
                    debug("Not loaded: "+gen['fb'][1], ERROR)

    def depRunner(self, block):
        ''' resolves the dependencies '''
        lst = [gen['subblock'] for gen in self.gen.featureBlock(self.dirtY)\
        if gen['block'] == block and gen['os'] == self._os[0]]

        for gen in self.gen.featureBlock(self.dirtY):
            if gen['os'] == self._os[0]:
                if gen['block'] == block or block == True:
                    if gen['fb'][0].lower() == 'dependencies':
                        for deps in gen['fb'][1]:
                            debug("["+gen['subblock']+"] depends on: "+deps, INFO)
                            self.deps.depGenAdd(gen['subblock'], deps)
                    else:
                            self.deps.depGenAdd(gen['subblock'])
                            
        depList = self.deps.dependencyGenRun()
        for revDep in depList[0]:
            self.workRunner(block, revDep)
        
            

    
                
                        
