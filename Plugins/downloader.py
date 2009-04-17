from threading import Thread
from Configurator import feature

class Downloader(Thread):
	#@feature('shovel.downloader')
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
        
        
