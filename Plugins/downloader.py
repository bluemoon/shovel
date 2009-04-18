from threading import Thread
from Messaging import CoreMessaging
from Configurator import Configurator
from Debug import Debug,GetDebug
import os
import urllib
import subprocess


class downloader(Thread):
	def __init__(self):
		self.Config = Configurator()
		self.CoreMessaging = CoreMessaging()
		Thread.__init__(self)
		
	def run(self):
		Attr = getattr(self,self.Command)
		Attr(self.Arguments,self.Filename,self.Name)
        
	def http(self,Name):
		Config = self.Config.GetConfig(Name)
		Debug(Config["link"],"DEBUG")
		Download = Config["link"]
		Filename = Config["link"].split("/")[-1:][0]
		print "[http] Downloading: " + Filename
		lib = os.path.isdir('tmp')
		Debug(os.getcwd(),"DEBUG")
		if not os.path.exists("tmp/" +Filename):
			if lib is False:
				os.mkdir('tmp')
				data = urllib.urlretrieve(Download, "tmp/" + Filename)
				urllib.urlcleanup()
			elif lib is True:
				data = urllib.urlretrieve(Download, "tmp/" + Filename)
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
		
		self.CoreMessaging.Send("downloader",Name+ ':done')

	def svn(self,Name):
		Config = self.Config.GetConfig(Name)
		Debug(Config["link"],"DEBUG")
		Download = Config["link"]
		Filename = Config["as"]
		Debug(Filename,"DEBUG")
		print "[svn] Checking out: " + Filename
		if not os.path.isdir(Filename):
			svnBuild = '/usr/bin/env svn co ' + Download + " tmp/" + Filename
			p = subprocess.Popen(svnBuild,shell=True,stdout=subprocess.PIPE)
			while p.stdout.readline():
				if p.stdout.readline() != "\n":
					if GetDebug() == "INFO" or GetDebug() == "WARNING" or GetDebug() == "DEBUG":
						print "[svn] " + p.stdout.readline()[:-1]
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done') 
		else:
			svnBuild = '/usr/bin/env svn up tmp/' + Filename
			p = subprocess.Popen(svnBuild,shell=True,stdout=subprocess.PIPE)
			while p.stdout.readline():
				if p.stdout.readline() != "\n":
					if GetDebug() == "INFO" or GetDebug() == "WARNING" or GetDebug() == "DEBUG":
						print "[svn] " + p.stdout.readline()
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done')
			 
	def git(self,Arguments,Filename,Name):
		if not os.path.isdir(Filename):
			gitBuild = '/usr/bin/env git clone ' + Arguments + " tmp/" + Filename
			p = subprocess.Popen(gitBuild,shell=True,stdout=None)
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done') 
		else:
			gitBuild = '/usr/bin/env git pull tmp/' + Filename
			p = subprocess.Popen(gitBuild,shell=True,stdout=subprocess.PIPE)
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done')
