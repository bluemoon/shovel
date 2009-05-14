import os

class chroot(object):
  def __init__(self):
    self.os = os.uname()[0]
    if self.os == 'Linux':
      self.x = Linux()
    elif self.os == 'Darwin':
      self.x = Linux()
  
  class Linux(object):
    def init(self):
      pass
  class Darwin(object):
    def init(self):
      pass
  
  def init(self):
    self.x.init()
    
