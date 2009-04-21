### System Imports ###
import time
### Local Imports ###
from CoreManifest import CoreElements


class CoreMessaging:
	# The class __impl is for the singleton
	# So we dont create more than one instance of this
	class __impl:
		def __init__(self):
			# Create the dictionary
			self.Fifo = {}
			# Iterate over all the core elements UI/Decoder/Audio/Lib..
			for M in CoreElements:
				# Create a list in each one of those elements to act
				# Like a queue
				self.Fifo[M] = []
			
		def Receive(self,CoreElement):
			# Here is the delay length to keep the CPU usage down
			delay = 0.015
			# This could potentially fail so its in a try catch
			try:
				# Wait for the message, 
				while len(self.Fifo[CoreElement]) == 0:
					#Keep the cpu usage down
					#delay = min(delay * 2, .05)
					time.sleep(delay)
				# Then return it once it gets one
				return self.Fifo[CoreElement].pop(0)
			except Exception,e:
				print e
		def ReceiveCheck(self,CoreElement):
			try:
				if len(self.Fifo[CoreElement]) > 0:
					return self.Fifo[CoreElement].pop(0)
				else:
					return False
			except Exception,e:
				print e
		def Send(self,CoreElement,Message):
			try:
				# Append to the CoreElement list.. ie.
				# UI/Decoder/Audio.... etc
				self.Fifo[CoreElement].append(Message)
				# I could check if CoreElement exists each time, which
				# could potentially be expensive, or i could assume it 
				# works and face the penalty
			except Exception,e:
				print e
				
			
	# The below is all the singleton work
	__instance = None
	
	def __init__(self):
		""" Create singleton instance """
		# Check whether we already have an instance
		if CoreMessaging.__instance is None:
			# Create and remember instance
			CoreMessaging.__instance = CoreMessaging.__impl()
			# Store instance reference as the only member in the handle
			self.__dict__['_CoreHandler__instance'] = CoreMessaging.__instance
	
	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)
	
	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
