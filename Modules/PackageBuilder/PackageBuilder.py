import os, sys
import subprocess
import tarfile
import urllib
import yaml
from threading import Thread
sys.path.append('Core')
from Messaging import CoreMessaging

CoreFeatureMap = { "download" : {"file" : "downloader", "class" : "Downloader"},
				   "extract"  : {"file" : "extractor" , "class" : "Extractor"},
				   "patch"	  : {"file" : "patcher"   , "class" : "Patcher"},
				   "build"    : {"file" : "builder"   , "class" : "Builder"},
}
CoreDependencies = dict(
					build    = ['download','patch','extract'],
					patch    = ['download','extract'],
					extract  = ['download'],
					download = []
)

class PackageBuilder(Thread):
	def __init__(self):
		self.CoreMessaging = CoreMessaging()
		self.Packages = {}
		self.PackageFeatures = {}
		
	def getPackages(self,Yaml):
		for PackageBuilder in Yaml:
			for Package in PackageBuilder:
				if 'package' in Package:
					for Iter in Package['package']:
						if 'name' in Iter:
							if Iter['name'] not in self.Packages:
								self.Packages[Iter['name']] = Package['package']
								#print self.Packages
	
	def getAllFeatures(self):
		"""docstring for getFeatures"""
		for Keys in self.Packages.keys():
			self.PackageFeatures[Keys] = []
			for List in self.Packages[Keys]:
				for Split in List['features'][0].split(" "):
					 self.PackageFeatures[Keys].append(Split.split(":"))
		#print self.PackageFeatures
			
	def NewMain(self,Yaml):
		self.getPackages(Yaml)
		self.getAllFeatures()
		PackageCounter = 0
		for Keys in self.PackageFeatures.keys():
			for List in self.PackageFeatures[Keys]:
				if List[0] == "download":
					for Package in self.Packages[Keys]:
						self.Downloader = Downloader(List[1],Package['download'],Package['filename'],Package['name'])
						PackageCounter += 1
						self.Downloader.start()
						
					Message = self.CoreMessaging.ReceiveCheck("downloader")
					if Message != False:
						PackageCounter = PackageCounter -1
						PackageFinish.append(Message.split(":")[0])
						print Message.split(":")[0] + ': Finished!'
						
	def Main(self,G_Yaml):
		if os.path.exists("dirt"):
			D = DispatchYaml()
			PackageFinish = []
			PackageCounter = 0
			#D.GetFeatures(G_Yaml,"ffmpeg")
			for Dirt in G_Yaml:
				for Package in Dirt['package']:
					PackageCounter += 1
					print Package['name'] + ": "
					FeatureList = Package['features'][0].split(" ")
					for F in FeatureList:
						Split = F.split(":")
						if Split[0] == "download":
							self.Downloader = Downloader(Split[1],Package['download'],Package['filename'],Package['name'])
							print "    Location: " + Package['download']
							self.Downloader.start()
							print "Downloading [" + Package['name'] +"] ...."
							Message = self.CoreMessaging.ReceiveCheck("downloader")
							if Message != False:
								PackageCounter = PackageCounter -1
								PackageFinish.append(Message.split(":")[0])
								print Message.split(":")[0] + ': Finished!'
                        
			while PackageCounter != 0:
				Message = self.CoreMessaging.Receive("downloader")
				PackageCounter = PackageCounter -1
				PackageFinish.append(Message.split(":")[0])
				print Message.split(":")[0] + ': downloaded ['+TermGreen+'ok'+TermEnd+']'
						
			for Dirt in G_Yaml:
				for Package in Dirt['package']:
					PackageCounter += 1
					FeatureList = Package['features']
					for F in FeatureList:
						for SpaceSplit in F.split(" "):
							Split = SpaceSplit.split(":") 
							if Split[0] == "extract":
								print Package['name'] + ': extracted ['+TermGreen+'ok'+TermEnd+']'
								self.Extractor = Extractor(Split[1],Package['filename'])
								self.Extractor.run()
									
			for Dirt in G_Yaml:
				for Package in Dirt['package']:
					FeatureList = Package['features']
					if Package['patches']:
						print Package['name'] + ': patching.'
						#print Package['patches']
						for Patch in Package['patches']:
							print '    Patch: ' + Patch + ' ['+TermGreen+'ok'+TermEnd+']'
							#self.Extractor = Patch(Split[1],Package['filename'])
							#self.Extractor.run()
					else:
						print Package['name'] + ': no patches to apply ['+TermGreen+'ok'+TermEnd+']'
			
			for Dirt in G_Yaml:
				for Package in Dirt['package']:
					FeatureList = Package['features']
					for F in FeatureList:
						for SpaceSplit in F.split(" "):
							Split = SpaceSplit.split(":") 
							if Split[0] == "build":
								print 'Building: ' + Package['name'] + ' using [' + Split[1] + ']'
								#self.Extractor = Extractor(Split[1],Package['filename'])
								#self.Extractor.run()
class Builder(Thread):
    def run(self,Command,Arguments):
        Attr = getattr(self,Command)
        Attr()
    def make(self):
        pass

class Downloader(Thread):
	def __init__(self,Command,Arguments,Filename,Name):
		self.Command = Command
		self.Arguments = Arguments
		self.Filename = Filename
		self.Name     = Name
		self.CoreMessaging = CoreMessaging()
		Thread.__init__(self)
        
	def run(self):
		Attr = getattr(self,self.Command)
		Attr(self.Arguments,self.Filename,self.Name)
        
	def http(self,Arguments,Filename,Name):
		lib = os.path.isdir('tmp')
		if not os.path.exists("tmp/" +Filename):
			if lib is False:
				os.mkdir('tmp')
				data = urllib.urlretrieve(Arguments, "tmp/" + Filename)
				urllib.urlcleanup()
			elif lib is True:
			  	data = 'Preexisting'
			if data is False:
				print 'Remote-retrieval: Download failure.'
			elif data is None:
				print 'Input error: No data for string.'
				
			urllib.urlcleanup()
			if data is False:
				return False
			else: 
				return True, lib
		
		self.CoreMessaging.Send("downloader",Name+ ':done')

	def svn(self,Arguments,Filename,Name):
		if not os.path.isdir(Filename):
			svnBuild = '/usr/bin/env svn co ' + Arguments + " tmp/" + Filename
			p = subprocess.Popen(svnBuild,shell=True,stdout=None)
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done') 
		else:
			svnBuild = '/usr/bin/env svn up tmp/' + Filename
			p = subprocess.Popen(svnBuild,shell=True,stdout=subprocess.PIPE)
			p.wait()
			self.CoreMessaging.Send("downloader",Name + ':done') 
        
        

class Extractor:
    def __init__(self,Command,File):
        self.Command = Command
        self.File    = File
    def run(self):
        Attr = getattr(self,self.Command)
        Attr(self.File)
        
    def tar(self,File):
        if os.path.exists("tmp/"+File):    
            End = File.split(".")
            if End[-1] == "bz2":
                tar = tarfile.open(name="tmp/" + File,mode='r:bz2')
                extract = tar.extractall(path="tmp",members=None)
            if End[-1] == "gz":
                tar = tarfile.open(name="tmp/" + File,mode='r:gz')
                extract = tar.extractall(path="tmp",members=None)

class Patcher:
	def __init__(self):
		self.Command = Command
		self.File    = File
	def patch(self,File):
		pass



class Dependencies:
	def __init__(self):
		self.DependencyList = {}
	def BuildCoreDependencies(self,CoreDep):
		self.DependencyList = CoreDep
	def DependencyGeneratorAdd(self,Dependant,DependsOn):
		self.DependencyList[Dependant] = DependsOn
	def DependencyGeneratorRun(self):
		D = dict((k, set(self.DependencyList[k])) for k in self.DependencyList)
		R = []
		while D:
			t = set(i for v in D.values() for i in v)-set(D.keys())
			t.update(k for k, v in D.items() if not v)
			R.append(t)
			D = dict(((k, v-t) for k, v in D.items() if v))
			return R


class DispatchYaml:
	def __init__(self, arg=None):
		self.arg = arg
	def ParseYaml(self,Yaml):
		#for Dirt in Yaml:
		pass
	def GetFeatures(self,Yaml,S_Package):
		Features = []
		FeatureI = 1
		#print Yaml
		Itr = 0
		for Dirt in Yaml:
			for Package in  Dirt['package']:
				#print Package
				if Package['name'] == S_Package:
					print Package['name']
					SpaceSplit = Package['features'][0].split(" ")
					for Colon in SpaceSplit:
						Features.append(Colon.split(":"))

		if not Features:
			return False
		else:
			return Features

		Itr = Itr + 1	

	def DispatchFeature(self,Feature,*Args):
		for CoreFeatures in CoreFeatureMap:
			if CoreFeatures == Feature:
				Md = sys.modules[CoreFeatureMap[CoreFeatures]['file']]
				DynamicClass = getattr(Md,CoreFeatureMap[CoreFeatures]['class'])
				dClassHandle = DynamicClass(Args)
				print dClassHandle.__dict__
			else:
				return False