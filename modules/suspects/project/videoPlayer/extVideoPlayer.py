'''Info Header Start
Name : extVideoPlayer
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''

class extVideoPlayer:
	"""
	extVideoPlayer description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		self.StatusCHOP = self.ownerComp.op('playback_state')
		#self.Player = self.ownerComp.op('moviefilein1')

	@property
	def Player(self):
		return self.ownerComp.op("repoMaker").Repo

	def Load(self, filepath):
		#self.Unload()
		self.Player.par.file = filepath
		self.Player.preload()

	def Unload(self):
		self.Player.unload()
		self.Player.par.play = False
		self.Player.par.file = ''
		
	def Execute_Trigger(self):
		self.ownerComp.op('callbackManager').Do_Callback("OnTrigger", self.ownerComp )

	def Start(self):
		self.Player.par.cuepulse.pulse()
		self.Player.par.play = True
		self.ownerComp.op('callbackManager').Do_Callback("OnPlayStart", self.ownerComp )

	def Stop(self, unload = True):
		self.Player.par.play = False
		if unload: self.Unload()

	def Pause(self):
		self.Stop( unload = False)