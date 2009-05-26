## File: Shovel.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/05/08
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
#### System Includes #########################################################
import sys
import os
import yaml
import subprocess
import optparse

    
####
## From Core
##

from Core.Configurator  import Configurator
from Core.Debug         import *
from Core.Plugin        import Plugin
from Core.File		import rmDirectoryRecursive
from Core.Lexer         import Lexi

## Attempt to speed this up a little
try:
    ## Psyco for a little more performance
    import psyco
    psyco.full()
except ImportError:
    debug("Psyco not loaded.",INFO)
else:
    debug("Psyco Enabled!",INFO)

##
# Global version string
VERSION = '0.0.1rc3'


class Shovel(object):
    ''' main class for the application '''
    def __init__(self):
        self.config = Configurator()
        self.plugins  = Plugin()
	
        
    def Arguments(self):
        ''' Handles all of the arguments to the program'''
        
    
        ## Usage string
        parser = self.parseOptions()
	self.options, self.remainder = parser.parse_args()
        
        
        ## Specifying your own dirt file
        if self.options.dirt:
            self.config.PutGlobal("dirt",self.options.dirt)
            
        ## Otherwise you get the default ;)
        else:
            self.config.PutGlobal("dirt",'dirt')
        ## For sandbox installs
        if self.options.sandbox:
            self.config.PutGlobal("sandbox",True)
    
        ## Disable formatting
        if self.options.nonpretty:
            self.config.PutGlobal("nonpretty",True)
        
        ## For debug verbosity
        if self.options.verbose:
            if int(self.options.verbose) > 3 or int(self.options.verbose) < 0:
                raise Exception('DebugLevelExceeded')
            self.config.PutGlobal("debug",self.options.verbose)

        ## For the new lexer
        if self.options.parser:
            self.config.PutGlobal("parser",self.options.parser)
        
        ## For the specified lexer
        if self.options.lexer:
            self.config.PutGlobal("lexer",self.options.lexer)
        else:
            self.config.PutGlobal("lexer",'yaml')
            
        ## Clean up the tmp/ directory    
        if self.options.clean:
            print "Cleaning up."
            rmDirectoryRecursive("tmp/")
            sys.exit(0)
            
        ## Run internal tests
        if self.options.tests:
            self.config.PutGlobal("tests",self.options.tests)
        
        ## For setting a config file
        if self.options.config:
            yOut = yaml.dump(self.config.getGlobalDump())
            fHandle = open('.shovel', 'w')
            fHandle.write(yOut)
            fHandle.close()

    
    def parseOptions(self):
        usage = "usage: %prog [options] module"
        parser = optparse.OptionParser(usage=usage, version=VERSION)
        parser.add_option('-d', '--dirt', action="store", dest="dirt", help="Specify the dirt file")
        parser.add_option('-v', action="store", dest="verbose", help="Changes the verbosity level")
        parser.add_option('--set-config', action="store_true", dest='config', help='Sets the config file')
        parser.add_option('--np', action="store_true", dest="nonpretty", help="Disables formatting")
        parser.add_option('--sandbox',action="store_true",dest="sandbox", help="Does a sandbox install")
        parser.add_option('-c', '--clean',action="store_true",dest="clean", help="Cleans the project")
        parser.add_option('--lexer', action="store", dest="lexer", help="Use the specified lexer")
        parser.add_option('--internal-tests', action="store_true", dest="tests", help="Run tests")
        return parser


        
    
    def Main(self):
        self.plugins.loadAll()
        
        if os.path.exists('.shovel'):
            dirtFile = open('.shovel', 'r')
            dFile = dirtFile.read()
            self.config.setGlobalDump(yaml.load(dFile,Loader=Loader))
        
        ## Parse the arguments
        self.Arguments()
        ## Debug tests
        
        ## debug('testing info',INFO)
        ## debug('testing warning',WARNING)
        ## debug('testing debug',DEBUG)
        
        newLex   = self.config.GetGlobal('parser')
        dirtFile = self.config.GetGlobal('dirt')
        lexer    = self.config.GetGlobal('lexer')
        tests    = self.config.GetGlobal('tests')
        
        ## --internal-tests
        if tests:
            Pry = subprocess.Popen('pry Tests -v',shell=True,stdout=None,stderr=None)
            Pry.wait()
        
        ## --new-lex
        if newLex:
            lexi = Lexi()
            lexi.loadLexer(str(dirtFile))
            lexi.runLexer()

        ## --lexer=lexer-name        
        if lexer and not newLex:
            if lexer == 'yaml':
                from Core.YamlParser import yamlParser
                yml = yamlParser()
                yml.main(str(dirtFile),self.remainder)
            if lexer == 'new':
                lexi = Lexi()
                lexi.loadLexer(str(dirtFile))
                lexi.runLexer()   

		

if __name__ == "__main__":
  M = Shovel()
  try:
    M.Main()
  except KeyboardInterrupt:
    print '\nExiting...'
    sys.exit(0)		
