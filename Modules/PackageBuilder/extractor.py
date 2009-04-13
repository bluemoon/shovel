import os, sys
import tarfile

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
