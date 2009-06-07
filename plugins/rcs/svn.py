class svn(object):
    """docstring for svn"""
    def __init__(self):
        try:
            import pysvn
            self.svn = pysvn()
        except ImportError:
            import subprocess
            self.svn = cl_svn()
        
    def checkout(self, http, directory, as_folder):
        self.svn.checkout(http, directory, as_folder)
        
    def update(self, directory):
        self.svn.update(directory)
        
    def commit(self, options):
        pass


class pysvn(object):
	"""docstring for pysvn"""
    def __init__(self):
        self.client = pysvn.Client()
        
    def checkout(self, http, location, as_folder):
        self.client.checkout(http, location)
        
    def update(self, location):
        self.client.update(location)
    def commit(self):
        
		
class cl_svn(object):
    def checkout(self, http, location, as_folder):
        svnBuild = '/usr/bin/env svn co %s %s %s' % (http, location, as_folder)
        p = subprocess.Popen(svnBuild, shell=True, stdout=subprocess.PIPE)
        while p.stdout.readline():
            if p.stdout.readline() != "\n":
                print "[svn] " + p.stdout.readline()[:-1]
                
        p.wait()
    def update(self, location):
        svnBuild = '/usr/bin/env svn update %s %s %s' % (http, location, as_folder)
        p = subprocess.Popen(svnBuild, shell=True, stdout=subprocess.PIPE)
        while p.stdout.readline():
            if p.stdout.readline() != "\n":
                print "[svn] " + p.stdout.readline()[:-1]
                
        p.wait()
