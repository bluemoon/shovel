import os
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
            pass
        else:
            dirtFile = open(fileName, 'r')
            dFile = dirtFile.read()
            self.dyaml = yaml.load(dFile)
            
    def run(self):
        for gen in yGen(self.dyaml):
            if isinstance(gen['keys'], dict):         
                if 'recipe' in gen['keys']:
                    self.recipe.runner(gen['keys']['recipe'])
            elif isinstance(gen['keys'], bool):
                pass
            elif '->' in gen['keys']:
                pass
                
                
        
