import os
import sys
import yaml

import core.recipe

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
        #print [[[j for j in k if 'recipe' not in j] for k in x.items()] for x in yGen(self.dyaml)]
        #print dict((x for x in v if 'recipe' in v ) for k,v in self.dyaml.items())
        block = {}        
        for generated in yGen(self.dyaml):
            if 'recipe' not in generated['keys']:
                if 'recipe' not in generated['subblock']:
                    print generated                   
                    #try:
                    #    block[generated['block']].append({generated['subblock']:generated['keys']})
                    #except KeyError:
                    #    block[generated['block']] = []
                    #    if generated['subblock'] not in block[generated['block']]:
                    #        block[generated['block']].append(generated['subblock'])

                    #    block[generated['block']][generated['subblock']].append(generated['keys'])

        print block
        for gen in yGen(self.dyaml):
            if isinstance(gen['keys'], dict):         
                if 'recipe' in gen['keys']:
                    try:
                        self.recipe.runner(gen['keys']['recipe'], block[gen['block']])
                    except KeyError:
                        self.recipe.runner(gen['keys']['recipe'])

            elif isinstance(gen['keys'], bool):
                pass
            elif '->' in gen['keys']:
                pass
                
                
        
