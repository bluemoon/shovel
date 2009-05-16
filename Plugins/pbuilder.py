from Core.Terminal     import TermGreen,TermEnd
from Core.Utils	       import pprint
from Core.Configurator import Configurator
from Core.Debug        import Debug,GetDebug
from threading         import Thread
from Core.Utils        import ProgressBar,RotatingMarker,ETA,FileTransferSpeed,Percentage,Bar

import os
import urllib
import subprocess
import sys
import tarfile
import re
import os
import subprocess


class make:
  def __init__(self):
    self.Config = Configurator()
    self.cwd = os.getcwd()
    self.sandbox_path = 'tmp/sandbox'
    
  def Configure(self,Directory,Configure):
    # If sandox is passed, prepare to build a sandbox
    if self.Config.GetGlobal("sandbox"):
      if not os.path.exists(self.sandbox_path):
        os.mkdir(self.sandbox_path)
      NewConfigure = "--prefix="+ self.cwd +"/" + self.sandbox_path  +" " + " ".join(Configure)
      Debug(NewConfigure,"DEBUG")
      Configure = NewConfigure
      
    # Otherwise pass the normal configure options
    else:
      Configure = " ".join(Configure)
    Debug("Changing to directory: " + self.cwd + '/tmp/downloads/' + Directory,"DEBUG")
    os.chdir(self.cwd + '/tmp/downloads/' + Directory)
    Debug("Configuring...","INFO")
    
    # If it has prepared options ie. --prefix.....
    if Configure:
      print "[make] Configure Options: " + Configure
      p = subprocess.Popen('./configure ' + Configure,shell=True,stdout=None)
      p.wait()
    # Otherwise configure it normally
    else:
      p = subprocess.Popen('./configure',shell=True,stdout=None)
      p.wait()
    
    Debug("Changing to directory: " + self.cwd ,"DEBUG")
    os.chdir(self.cwd)
    
  def Build(self,Directory):
    Debug("Changing to directory: " + self.cwd + '/tmp/downloads/' + Directory,"DEBUG")
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
    Debug("Build Return Code: %d" % (MakeSub.returncode),"INFO")
    if MakeSub.returncode > 0:
      raise Exception('BuildError')
		
    if self.Config.GetGlobal("sandbox"):
      Debug("Sandbox Install","INFO")
      SB = subprocess.Popen('make install',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      SB.wait()
    
    Debug("Changing to directory: " + self.cwd,"DEBUG")
    os.chdir(self.cwd)
    
class waf:
  def __init__(self):
    self.cwd = os.getcwd()

  def Configure(self,Directory):
    Debug("waf configuring","DEBUG")
    Debug("waf changing directory [" +self.cwd + Directory+ "]","DEBUG")
    os.chdir(self.cwd + Directory)
    wafConfigure = subprocess.Popen('./waf configure ',shell=True,stdout=None)
    wafConfigure.wait()
    Debug("waf changing directory [" +self.cwd  +"]","DEBUG")
    os.chdir(self.cwd)

  def Build(self,Directory):
    Debug("waf building","DEBUG")
    Debug("waf changing directory [" +self.cwd + Directory+ "]","DEBUG")
    os.chdir(self.cwd + Directory)
    wafBuild = subprocess.Popen('./waf build',shell=True,stdout=None)
    wafBuild.wait()
    Debug("waf changing directory [" +self.cwd +"]","DEBUG")
    os.chdir(self.cwd)

class builder:
  def __init__(self):
    self.Config = Configurator()

  def waf(self,Name):
    Debug(Name,"DEBUG")
    Config = self.Config.GetConfig(Name)
    Folder = Config["folder"]
    w = waf()
    print "[waf] Configure: " 
    w.Configure(Folder)
    print "[waf] Build: "
    w.Build(Folder)
  
  def make(self,Folder,Configure,Name):
    Debug(Name,"DEBUG")
    m = make()
    print "[make] Configure" 
    m.Configure(Folder,Configure)
    print "[make] Build" 
    m.Build(Folder)

def ExtractNameFromTar(Tar):
	Tar = Tar.split(".")[:-2]
	return ".".join(Tar)
	
def locate(pattern, root=os.getcwd()):
	for path, dirs, files in os.walk(root):
		for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
			yield filename
			
def IntelliPatcher(PatchFile):
	Pmatch = re.compile('(\+|\-){3}\s[a-zA-Z0-9_/\.-]*')
	FileM = re.compile('[a-zA-Z0-9_/\.-]*')
	File = open(PatchFile,"r")
	while File.readline():
		Line = File.readline()
		G = Pmatch.match(Line)
		if G:
			print G.group()
	for C in locate("*.c","tmp"):
		print C
			

class patcher(object):
	def __init__(self):
		self.Config = Configurator()
	def patch(self,Name):
		Config = self.Config.GetConfig(Name)
		self.Config.CreateOutYaml(Name)
		Folder = self.Config.FindInPackage("extract",Name)
		PatchDir = ExtractNameFromTar(Folder['file'])
		CWD = os.getcwd()
		os.chdir("tmp/downloads/" + PatchDir)
		for File in Config["file"]:
			#IntelliPatcher(Files)
			PatchLevel =  File.split('@')
			pLevel = PatchLevel[1].split(':')[1]
			pFile  = PatchLevel[0]
			Patch = subprocess.Popen('patch -p%d < %s' % (int(pLevel),CWD+"/"+pFile),shell=True,stdout=None,stderr=None)
			Patch.wait()
			if Patch.returncode > 0:
				Debug("Patch didn't return 0!","WARNING")
		os.chdir(CWD)
		#Debug(Config["link"],"DEBUG")
		
def ExtractNameFromTar(Tar):
	Tar = Tar.split(".")[:-2]
	return ".".join(Tar)

class extractor:
	def __init__(self):
		self.Config = Configurator()

	def tar(self,Filename,Name):
		Tar = {}
		#Config = self.Config.GetConfig(Name)
		#Debug(Config,"DEBUG")
	 	#File = Config["file"]
		File = Filename
		self.Config.CreateOutYaml(Name)
		if not os.path.exists("tmp/downloads/" + ExtractNameFromTar(File)):
			print "[tar] Extracting: " + File
			if os.path.exists("tmp/downloads/" + File):
				End = File.split(".")
				if End[-1] == "bz2":
					tar = tarfile.open(name="tmp/downloads/" + File,mode='r:bz2')
					try:
						extract = tar.extractall(path="tmp/downloads/",members=None)
					except EOFError,e:
						print "The file appears to be corrupt, run with",
						print "--clean and then retry building"
						Debug(e,"ERROR")
						sys.exit(0)
				if End[-1] == "gz":
					tar = tarfile.open(name="tmp/downloads/" + File,mode='r:gz')
					try:
						extract = tar.extractall(path="tmp/downloads/",members=None)
					except EOFError,e:
						print "The file appears to be corrupt, run with",
						print "--clean and then retry building"
						Debug(e,"ERROR")
						sys.exit(0)

def md5(File,Against):
  import hashlib
  m = hashlib.md5()
  try:
    fd = open(File,"rb")
  except IOError:
    print "Unable to open the file in readmode:", filename
    return
  content = fd.readlines()
  fd.close()
  for eachLine in content:
    m.update(eachLine)
  Digest = m.hexdigest()
  if Against == Digest:
    return True
  else:
    return Digest

def _reporthook(numblocks, blocksize, filesize, url,pbar):
  pbar.update((numblocks*blocksize*100)/filesize)

class downloader(Thread):
  def __init__(self):
    self.Config = Configurator()
    Thread.__init__(self)

  def http(self,Name):
    Config = self.Config.GetConfig(Name)
    Debug(Config["link"],"DEBUG")
    Download = Config["link"]
    Filename = Config["link"].split("/")[-1:][0]
    

    
    print "[http] Downloading: " + Filename
		
    tmp = os.path.isdir('tmp/')
    lib = os.path.isdir('tmp/downloads/')
		
    if not tmp:
      os.mkdir('tmp')
    Debug(os.getcwd(),"DEBUG")
		
    self.Config.CreateOutYaml(Name)
		
    if not os.path.exists("tmp/downloads/" +Filename):
      if lib is False:
        os.mkdir('tmp/downloads/')
        widgets = [Filename + " ", Percentage(), ' ', Bar(),' ', ETA(), ' ', ' ']
        pbar = ProgressBar(widgets=widgets).start()
        data = urllib.urlretrieve(Download, "tmp/downloads/" + Filename,lambda nb, bs, fs, url=Download: _reporthook(nb,bs,fs,url,pbar))
        pbar.finish()
        print
        urllib.urlcleanup()
      elif lib is True:
        widgets = [Filename + " ", Percentage(), ' ', Bar(),' ', ETA(), ' ', ' ']
        pbar = ProgressBar(widgets=widgets).start()
        data = urllib.urlretrieve(Download, "tmp/downloads/" + Filename,lambda nb, bs, fs, url=Download: _reporthook(nb,bs,fs,url,pbar))
        pbar.finish()
        print
        urllib.urlcleanup()
        Debug("Folder tmp is pre-existing","INFO")
        data = 'Preexisting'
      if data is False:
        Debug('Remote-retrieval: Download failure.',"ERROR")
      elif data is None:
        Debug('Input error: No data for string.',"ERROR")
				
      urllib.urlcleanup()
      if data is False:
        return False
      else: 
        return True, lib

    
		  
    Down = {"downloader":True}		
    self.Config.AppendOutYaml(Name,Down)


  def svn(self,Name):
    Config = self.Config.GetConfig(Name)
    Debug(Config["link"],"DEBUG")
    Download = Config["link"]
    Filename = Config["as"]
    Debug(Filename,"DEBUG")
    print "[svn] Checking out: " + Filename
    if not os.path.isdir(Filename):
      svnBuild = '/usr/bin/env svn co ' + Download + " tmp/downloads/" + Filename
      p = subprocess.Popen(svnBuild,shell=True,stdout=subprocess.PIPE)
      while p.stdout.readline():
        if p.stdout.readline() != "\n":
          if GetDebug() == "INFO" or GetDebug() == "WARNING" or GetDebug() == "DEBUG":
            print "[svn] " + p.stdout.readline()[:-1]
      p.wait()

    else:
      svnBuild = '/usr/bin/env svn up tmp/downloads/ '+ Filename
      p = subprocess.Popen(svnBuild,shell=True,stdout=subprocess.PIPE)
      while p.stdout.readline():
        if p.stdout.readline() != "\n":
          if GetDebug() == "INFO" or GetDebug() == "WARNING" or GetDebug() == "DEBUG":
            print "[svn] " + p.stdout.readline()
      p.wait()

			 
  def git(self,Arguments,Filename,Name):
    if not os.path.isdir(Filename):
      gitBuild = '/usr/bin/env git clone ' + Arguments + " tmp/downloads/" + Filename
      p = subprocess.Popen(gitBuild,shell=True,stdout=None)
      p.wait()
    else:
      gitBuild = '/usr/bin/env git pull tmp/downloads/' + Filename
      p = subprocess.Popen(gitBuild,shell=True,stdout=subprocess.PIPE)
      p.wait()


class pbuilder(object):
  def __init__(self):
    self.Config = Configurator()
    
  def build(self,Name):
    Config = self.Config.GetConfig(Name)
    Filename = Config["link"].split("/")[-1:][0]
    Configuration = Config['configure']
    try:
      Md5 = Config["md5"]
    except Exception, E:
		  Md5 = None
		  
    d = downloader()
    d.http(Name)
    
    if Md5:
      Digest = md5("tmp/downloads/" + Filename,Md5)
      if Digest == True:
        print '[md5]: %s digests match. download fine. ' % (Md5)
      else:
        print 'Digest failed got: %s expected: %s' % (Digest,Md5)
        raise Exception('md5DigestError') 
        
    e = extractor()
    e.tar(Filename,Name)
    Folder = ExtractNameFromTar(Filename)
    
    Debug('Adding ' + os.getcwd() + '/tmp/sandbox/lib/pkgconfig/ to PKG_CONFIG_PATH')
    pkgCfg = subprocess.Popen('export PKG_CONFIG_PATH=' + os.getcwd() + '/tmp/sandbox/lib/pkgconfig/',shell=True,stdout=None)
    pkgCfg.wait()
    
    b = builder()
    b.make(Folder,Configuration,Name)
    
    
    
