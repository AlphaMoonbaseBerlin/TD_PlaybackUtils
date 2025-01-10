'''Info Header Start
Name : extTimedVideoPlayer
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''


class extTimedVideoPlayer:
	"""
	extTimedVideoPlayer description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def Player(self):
		return self.ownerComp.op("playerRepoMaker").Repo

	@property
	def Timer(self):
		return self.ownerComp.op("timerRepoMaker").Repo

	@property
	def Timecode(self):
		return self.ownerComp.op("timecode")

	@property
	def Length(self):
		length = tdu.Timecode(
					frame = self.Player.numImages if self.Player.numImages > 1 else int(self.ownerComp.par.Imagetime.eval() * self.Player.rate), 
					fps = self.Player.rate 
				)
		length.fps = project.cookRate
		return length

	
	@property
	def callback(self):
		return self.ownerComp.op("callbackManager")

	@property
	def Ready(self):
		return bool( self.ownerComp.op("openingStatus")[0].eval() )

	@property
	def Idle(self):
		return not self.Player.par.file.eval() and not self.Ready

	@property
	def Running(self):
		return bool( self.Timer["running"].eval() )

	def onReady(self):
		""" Preparing all elements to get started."""
		self.Player.par.playmode.val = 3
		self.Player.par.timecodeop.val = self.Timecode

		self.Timer.par.lengthunits.val = 1
		self.Timer.par.length = self.Length.totalFrames
		self.Timer.par.cycle.val = True
		self.Timer.par.maxcycles.val = 1
		self.Timer.par.cycleendalert.val = self.ownerComp.par.Triggertime.eval()
		self.Timer.par.cyclelimit.val = True
		self.Timer.par.initialize.pulse()
		self.callback.Do_Callback("onReady", self.Player, self.ownerComp)
		if self.ownerComp.par.Autostart.eval(): self.Start()


	def onTrigger(self):
		self.callback.Do_Callback("onTrigger", self.Player, self.ownerComp)
		return

	def onStart(self):
		self.callback.Do_Callback("onStart", self.Player, self.ownerComp)
		return
	
	def onDone(self):
		self.callback.Do_Callback("onDone", self.Player, self.ownerComp)
		if self.ownerComp.par.Autounload.eval(): self.Unload()
		return

	def onError(self):
		self.callback.Do_Callback("onError", self.Player, self.ownerComp)
		return

	def Start(self):
		self.Timer.par.start.pulse()

	def Load(self, filepath):
		self.Player.par.file.val = filepath
		if self.ownerComp.par.Preload.eval():
			self.Player.preload()

	def Unload(self):
		self.Player.par.file.val = ""