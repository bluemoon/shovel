import subprocess

class UnixWrapper:
  def __init__(self):
    self.Command = ''
    self.Command_Location  = ''
    self.Command_Arguments = ''
  def run(self,Wait=True):
    run = subprocess.Popen(self.Command + self.Command_Location 
    + self.Command_Arguments,shell=True,stdout=None)
    
    if Wait:
      run.wait()
