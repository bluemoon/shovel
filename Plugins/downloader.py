from threading import Thread
from Core.Configurator import Configurator
from Core.Debug import *
from Core.Utils import ProgressBar,RotatingMarker,ETA,FileTransferSpeed,Percentage,Bar
import os
import urllib
import subprocess
import sys
import sys


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
    try:
      Md5 = Config["md5"]
    except Exception, E:
		  Md5 = None

    
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

    if Md5:
      Digest = md5("tmp/downloads/" + Filename,Md5)
      if Digest == True:
        print '[md5]: %s digests match. download fine. ' % (Md5)
      else:
        print 'Digest failed got: %s expected: %s' % (Digest,Md5)		 
        raise Exception('md5DigestError') 
		  
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

