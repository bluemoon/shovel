##############################################################################
## File: builder.py
## Version: -*-dev-*-
## Author: Alex Toney (toneyalex@gmail.com)
## Date: 2009/04/22
## Copyright (c) 2009 Alex Toney
## License: GPLv2 (http://www.gnu.org/licenses/gpl-2.0.html)
##############################################################################

#### System Imports ##########################################################
import os
import subprocess
import re
#### Local Imports ###########################################################
from Core.Configurator import Configurator
from Core.Debug        import *
from Core.Terminal     import TermGreen,TermEnd
from Core.Utils	       import pprint

class make:
  def __init__(self):
    self.Config = Configurator()
    self.cwd = os.getcwd()
    self.sandbox_path = 'tmp/sandbox'
    
  def Configure(self, Directory, Configure):
    # If sandox is passed, prepare to build a sandbox
    if self.Config.GetGlobal("sandbox"):
      if not os.path.exists(self.sandbox_path):
        os.mkdir(self.sandbox_path)
      NewConfigure = "--prefix="+ self.cwd +"/" + self.sandbox_path  +" " + " ".join(Configure)
      debug(NewConfigure, DEBUG)
      Configure = NewConfigure
      
    # Otherwise pass the normal configure options
    else:
      Configure = " ".join(Configure)
      
    debug("Changing to directory: " + self.cwd + '/tmp/downloads/' + Directory, DEBUG)
    os.chdir(self.cwd + '/tmp/downloads/' + Directory)
    debug("Configuring...", INFO)
    
    # If it has prepared options ie. --prefix.....
    if Configure:
      print "[make] Configure Options: " + Configure
      p = subprocess.Popen('./configure ' + Configure,shell=True,stdout=None)
      p.wait()
    # Otherwise configure it normally
    else:
      p = subprocess.Popen('./configure',shell=True,stdout=None)
      p.wait()
    
    debug("Changing to directory: " + self.cwd , DEBUG)
    os.chdir(self.cwd)
    
  def Build(self, Directory):
    debug("Changing to directory: " + self.cwd + '/tmp/downloads/' + Directory, DEBUG)
    os.chdir(self.cwd + '/tmp/downloads/' + Directory)
    #Debug("Building:" + Name,"INFO")
    #print "[make] Building: " + Name
    regex = re.compile('[a-zA-Z0-9/_]*\.c')
    if self.Config.GetGlobal("nonpretty"):
      MakeSub = subprocess.Popen('make',shell=True,stdout=None,stderr=None)
    else:
      MakeSub = subprocess.Popen('make',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      while MakeSub.poll() is None:
        Read = MakeSub.stdout.readline()
        match = regex.findall(Read)
        if match:
          pprint("Compiling: " + match[0],"ok",None,"GREEN")
        else:
          pprint("Out: "+Read[:-1],"!!","BLUE","BLUE")
          
    MakeSub.wait()
    # Make sure the build returns a valid code and doesnt fail
    debug("Build Return Code: %d" % (MakeSub.returncode), INFO)
    if MakeSub.returncode > 0:
      raise Exception('BuildError')
    
    if self.Config.GetGlobal("sandbox"):
      debug("Sandbox Install", INFO)
      SB = subprocess.Popen('make install',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      SB.wait()
    
    debug("Changing to directory: " + self.cwd, DEBUG)
    os.chdir(self.cwd)
    
class waf:
  def __init__(self):
    self.cwd = os.getcwd()

  def Configure(self,Directory):
    debug("waf configuring", DEBUG)
    debug("waf changing directory [" +self.cwd + Directory+ "]", DEBUG)
    
    os.chdir(self.cwd + Directory)
    wafConfigure = subprocess.Popen('./waf configure ',shell=True,stdout=None)
    wafConfigure.wait()
    
    debug("waf changing directory [" +self.cwd  +"]", DEBUG)
    os.chdir(self.cwd)

  def Build(self,Directory):
    debug("waf building", DEBUG)
    debug("waf changing directory [" +self.cwd + Directory+ "]", DEBUG)
    
    os.chdir(self.cwd + Directory)
    wafBuild = subprocess.Popen('./waf build',shell=True,stdout=None)
    wafBuild.wait()
    
    debug("waf changing directory [" +self.cwd +"]", DEBUG)
    os.chdir(self.cwd)

class builder:
  def __init__(self):
    self.Config = Configurator()

  def waf(self,Name):
    debug(Name, DEBUG)
    
    Config = self.Config.GetConfig(Name)
    Folder = Config["folder"]
    w = waf()
    print "[waf] Configure: " 
    w.Configure(Folder)
    print "[waf] Build: "
    w.Build(Folder)
  
  def make(self,Name):
    Debug(Name, DEBUG)
    # Get all the info from the container class
    Config = self.Config.GetConfig(Name)
    Debug(Config, DEBUG)
    # Get the function parameters from the container class
    File = Config["folder"]
    Configure = Config["configure"]
    m = make()
    
    print "[make] Configure" 
    m.Configure(File, Configure)
    print "[make] Build" 
    m.Build(File)

