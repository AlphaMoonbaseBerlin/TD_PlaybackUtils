'''Info Header Start
Name : extMoviefileInController
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''
"""
Help: search "Extensions" in wiki
"""

class extMoviefileInController:
	"""
	extMoviefileInController description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp


	@property
	def Target(self) -> moviefileinTOP:
		return self.ownerComp.par.Target.eval()

	def Play(self, restart = True):
		if restart: self.Target.par.cuepulse.pulse()
		self.Target.par.play.val = True
		return
	
	def Stop(self, reset = False):
		if reset: self.Target.par.cuepulse.pulse()
		self.Target.par.play.val = False

	def Load(self, filepath):
		self.Target.par.file.val = filepath

	def Unload(self):
		self.Target.par.file.val = ""

	def Preload(self):
		self.Target.preload()
	
	def ExecuteCallback(self, callbackName):
		self.ownerComp.op("logger").Log("Executing Callback", callbackName)
		self.ownerComp.op("callbackManager").Do_Callback( f"on{callbackName}", self.Target, self.ownerComp)