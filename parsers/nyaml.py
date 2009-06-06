import os
import sys
import yaml

import core.recipe
from core.debug import *

def yGen(dictionary):
    for block, a in reversed(dictionary.items()):
        for subblock, b in a.items():
            yield {
                'block'    : block,
                'subblock' : subblock,
                'keys'     : b
                }

class nyaml:
    def __init__(self):
        self.recipe = core.recipe.recipe()
        
    def load(self, fileName):
        """ Load the dirt fileName """
        if not os.path.exists(fileName):
            print 'no file inputted!...'
            sys.exit(-1)
        else:
            dirtFile = open(fileName, 'r')
            dFile = dirtFile.read()
            self.dyaml = yaml.load(dFile)
            
    def run(self):
        ''' runs all of the blocks of yaml code '''
        block = {}
        for blck, a in reversed(self.dyaml.items()):
            for subblock, b in a.items():
                if isinstance(b, dict):
                    for feature, value in b.items():
                        if 'recipe' not in feature:
                            try:
                                block[subblock].append({feature:value})
                            except KeyError:
                                block[subblock] = []
                                block[subblock].append({feature:value})

                else:
                    if 'recipe' not in subblock:
                        try:
                            block[blck].append({subblock:b})
                        except KeyError:
                            block[blck] = []
                            block[blck].append({subblock:b})



        for gen in yGen(self.dyaml):
            if isinstance(gen['keys'], dict):         
                if 'recipe' in gen['keys']:
                    try:
                        debug(block[gen['subblock']], DEBUG)
                        if block.has_key(gen['subblock']):
                            self.recipe.runner(gen['keys']['recipe'], block[gen['subblock']])
                        if block.has_key(gen['block']):
                            self.recipe.runner(gen['keys']['recipe'], block[gen['block']])
                            
                    except KeyError:
                        self.recipe.runner(gen['keys']['recipe'])

            elif isinstance(gen['keys'], bool):
                pass
            elif '->' in gen['keys']:
                thenCount = 1
                thenList = gen['keys'].split('->')
                then = []
                for thenItr in thenList:
                    if not thenCount % 2:
                        if thenItr[:1] == ' ':
                            thenItr = thenItr[1:]
                    else:
                        if thenItr[:-1] == ' ':
                            thenItr = thenItr[-1:]
                            
                    then.append(thenItr)
                    thenCount = thenCount + 1  
                    
                for recipe in then:
                    try:
                        if block.has_key(gen['subblock']):
                            self.recipe.runner(gen['keys'], block[gen['subblock']])
                        if block.has_key(gen['block']):
                            self.recipe.runner(gen['keys'], block[gen['block']])
                        
                    except Exception, E:
                        debug(E, ERROR)
                        debug('%s failed so any dependants will not run' % (recipe), ERROR)
                        sys.exit(-1)
                        
                
                
        
