import os

import yaml

def yGen(dictionary):
    for block, a in dictionary.items():
        for subblock, b in a.items():
            yield {
                'block'    : block,
                'subblock' : subblock,
                'keys'     : b
                }

class nyaml:
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
            print gen
        
