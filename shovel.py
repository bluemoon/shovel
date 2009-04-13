### System Includes ###
import sys
import os
import yaml
import threading
import imp
from threading import Thread

sys.path.append('ModularCore')
sys.path.append('Core')
#### From ModularCore ####
from downloader import Downloader
from extractor  import Extractor
from builder    import Builder
from patcher	import Patcher
#### From Core ####
from Messaging  import CoreMessaging

### For the term coloring ###
TermGreen = "\033[1;32m"
TermEnd   = "\033[1;m"

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
		#self.Builder       = Builder()
		self.CoreMessaging = CoreMessaging()
	def Main(self):
		if os.path.exists("dirt"):
			D = DispatchYaml()
			PackageFinish = []
			DirtFile = open('dirt', 'r')
			DFile = DirtFile.read()
			G_Yaml = yaml.load(DFile)
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
		
if __name__ == "__main__":
    M = PackageBuilder()
    M.Main()
