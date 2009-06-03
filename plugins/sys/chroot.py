import os
import fcntl
import shutil
import stat
import subprocess
import re

import core.file as file

from core.debug import *
## to build with gcc:
##  
##
class chroot(object):
    def __init__(self):
        
        self.os = os.uname()[0]
        if self.os == 'Linux':
            self.x = self.Linux()
        elif self.os == 'Darwin':
            self.x = self.Darwin()
  
    class Linux(object):
        def __init__(self):
            ## Config options
            self.baseDir      = 'tmp/chroot'
            self.useResolv   = True
            self.internalDev = False

            self.umountCmds = [
                'umount -n %s' % file.buildPath(self.baseDir,'proc'),
                'umount -n %s' % file.buildPath(self.baseDir,'sys')
               ]
               
            self.mountCmds = [
                'mount -n -t proc   chroot_proc   %s' % file.buildPath(self.baseDir,'proc'),
                'mount -n -t sysfs  chroot_sysfs  %s' % file.buildPath(self.baseDir,'sys'),
               ]
        
        def _lddGet(self,binary):
             which = subprocess.Popen('which %s' % (binary), shell=True, stdout=subprocess.PIPE)
             which.wait()
             wOut = which.communicate()
             
             ldd = subprocess.Popen('ldd %s' % (wOut[0][:-1]), shell=True, stdout=subprocess.PIPE)
             ldd.wait()
             lOut = ldd.communicate()
             
             for all in lOut:
                if all:
                    matchFolder = re.compile('[a-zA-Z0-9\-\./]*')
                    if matchFolder:
                        m =  matchFolder.findall(all)
             
             for match in m:
                if match:
                    isHex = re.compile('0x[0-9a-f]')
                    hex = isHex.match(match)
                    if not hex:
                        print match

                
             
                   
        def _getChrootLock(self):
            ''' Tries to establish a lock for the chroot '''
            try:
                self.chrootLock = open(os.path.join(self.baseDir, "chroot.lock"), "a+")
            except IOError, e:
                return e

            try:
                fcntl.lockf(self.chrootLock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError, e:
                raise Exception("chroot is locked by another process.")

            return True
        
        def _mountAll(self):
            for cmd in self.mountCmds:
                subprocess.Popen(cmd, shell=True)
                
        def _unmountAll(self):
            for cmd in self.umountCmds:
                subprocess.Popen(cmd, shell=True)  
        def _ownAll(self):
            chPath = self.baseDir
            
        def _copyDirs(self):
            copyDirs = [
                'bin', 'usr/bin'
            ]
            for dir in copyDirs:
                rPath  = file.buildPath('/',dir)
                chPath = file.buildPath(self.baseDir,dir)
                ## if os.path.exists(chPath):
                ##     os.remove(chPath)
                
                debug('%s --> %s' % (rPath,chPath), DEBUG)
                shutil.copytree(rPath,chPath)
                
        def _setupDev(self):
        
            ## Clean up dev
            file.rmDirectoryRecursive(file.buildPath(self.baseDir,"dev"))
            file.mkdirIfAbsent(file.buildPath(self.baseDir,"dev", "pts"))
            file.mkdirIfAbsent(file.buildPath(self.baseDir,"dev", "shm"))
            
            prevMask = os.umask(0000)
            devFiles = (
                (stat.S_IFCHR | 0666, os.makedev(1, 3), "dev/null"),
                (stat.S_IFCHR | 0666, os.makedev(1, 7), "dev/full"),
                (stat.S_IFCHR | 0666, os.makedev(1, 5), "dev/zero"),
                (stat.S_IFCHR | 0666, os.makedev(1, 8), "dev/random"),
                (stat.S_IFCHR | 0444, os.makedev(1, 9), "dev/urandom"),
                (stat.S_IFCHR | 0666, os.makedev(5, 0), "dev/tty"),
                (stat.S_IFCHR | 0600, os.makedev(5, 1), "dev/console"),
                (stat.S_IFCHR | 0666, os.makedev(5, 2), "dev/ptmx"),
            )
            
            for i in devFiles:
                ## create node
                os.mknod(file.buildPath(self.baseDir, i[2]), i[0], i[1])
                ## set context. (only necessary if host running selinux enabled.)
                ## fails gracefully if chcon not installed.
                ## subprocess.Popen(
                ##    ["chcon", "--reference=/%s"% i[2], self.makeChrootPath(i[2])]
                ##    , raiseExc=0, shell=False)
            
            ## create all the stdin/stdout/stderr devices
            os.symlink("/proc/self/fd/0", file.buildPath(self.baseDir,"dev/stdin"))
            os.symlink("/proc/self/fd/1", file.buildPath(self.baseDir,"dev/stdout"))
            os.symlink("/proc/self/fd/2", file.buildPath(self.baseDir,"dev/stderr"))
            os.umask(prevMask)
            
            devUnMount = [
                'umount -n %s' % file.buildPath(self.baseDir,'/dev/pts'),
                'umount -n %s' % file.buildPath(self.baseDir,'/dev/shm')
            ]
            devMount = [
                'mount -n -t devpts chroot_devpts %s' % file.buildPath(self.baseDir,'/dev/pts'),
                'mount -n -t tmpfs  chroot_shmfs %s'  % file.buildPath(self.baseDir,'/dev/shm')
            ]
            
            ## mount/umount
            for cmd in devUnMount:
                if cmd not in self.umountCmds:
                    self.umountCmds.append(cmd)
            
            for cmd in devMount:
                if cmd not in self.mountCmds:
                    self.mountCmds.append(cmd)      
                  
        def init(self, location=None):
            if not location:
                self.baseDir = location
            
            debug('attempting to lock chroot',DEBUG)
            lock = self._getChrootLock()
            if lock == True:
                debug('got lock',DEBUG)                
            
            debug('creating base directory if needed',DEBUG)
            file.mkdirIfAbsent(self.baseDir)
            
            
            systemDirectories = [
            'dev', 'opt', 'sbin',
            'sbin', 'sys','lib','proc', 'etc',
            'usr/lib'
            ]
            
            debug('creating skeleton directories',DEBUG)
            ## build all the directories
            for dir in systemDirectories:
                built = file.buildPath(self.baseDir,dir)    
                file.mkdirIfAbsent(built)
           
            ## essential files
            essentialFiles = [
                file.buildPath(self.baseDir,'etc','mtab'),
                file.buildPath(self.baseDir,'etc','fstab'),
            ]
            map(file.touch,essentialFiles)
            
            ## if you want to use /etc/resolv.conf
            if self.useResolv:
                resolvPath = file.buildPath(self.baseDir,'etc','resolv.conf')
                resolvDir  = file.buildPath(self.baseDir,'etc')
                
                ## delete if it does exist
                if os.path.exists(resolvPath):
                    os.remove(resolvPath)
                    
                ## copy from your base system    
                shutil.copy2('/etc/resolv.conf', resolvDir)

            ## self._copyDirs()    

            if self.internalDev:
                self._setupDev()
            
            ## try:
            ##  self._mountall()
            ##  if not self.chrootWasCleaned:
            ##    self.chroot_setup_cmd = 'update'
            ##    self._yum(self.chroot_setup_cmd, returnOutput=1)
            ## finally:
            ##   self._umountall()
            
            localTimeDir  = file.buildPath(self.baseDir,'etc')
            localTimePath = file.buildPath(self.baseDir,'etc', 'localtime')
            if os.path.exists(localTimePath):
                os.remove(localTimePath)
            
            shutil.copy2('/etc/localtime', localTimeDir)
            
            self._lddGet('gcc')
            self._lddGet('ls')
                     
    class Darwin(object):
        def init(self):
            pass
  
    def init(self,directory):
        self.x.init(directory)
    
