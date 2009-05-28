from Core.Configurator import Configurator
from Core.Debug import *
import os
import sys
import tarfile

def ExtractNameFromTar(Tar):
    Tar = Tar.split(".")[:-2]
    return ".".join(Tar)

class extractor:
    def __init__(self):
        self.Config = Configurator()

    def tar(self, Name, filename=None):
        Tar = {}
        Config = self.Config.GetConfig(Name)
        debug(Config, DEBUG)
        File = Config["file"]

        if filename:
            File = Filename

        self.Config.CreateOutYaml(Name)
        if not os.path.exists("tmp/downloads/"+ExtractNameFromTar(File)):
            print "[tar] Extracting: " + File
            if os.path.exists("tmp/downloads/"+File):
                End = File.split(".")
                if End[-1] == "bz2":
                    tar = tarfile.open(name="tmp/downloads/" + File,mode='r:bz2')
                    try:
                        extract = tar.extractall(path="tmp/downloads/",members=None)
                    except EOFError,e:
                        print "The file appears to be corrupt, run with",
                        print "--clean and then retry building"
                        debug(e, ERROR)
                        sys.exit(0)
                if End[-1] == "gz":
                    tar = tarfile.open(name="tmp/downloads/" + File,mode='r:gz')
                    try:
                        extract = tar.extractall(path="tmp/downloads/",members=None)
                    except EOFError,e:
                        print "The file appears to be corrupt, run with",
                        print "--clean and then retry building"
                        debug(e, ERROR)
                        sys.exit(0)