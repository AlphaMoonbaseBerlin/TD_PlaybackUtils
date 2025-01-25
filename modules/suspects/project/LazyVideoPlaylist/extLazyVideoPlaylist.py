'''Info Header Start
Name : extLazyVideoPlaylist
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.11880
Info Header End'''

class extLazyVideoPlaylist:
	"""
	extLazyVideoPlaylist description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.log = self.ownerComp.op("logger").Log
		self.Reset()
		
	@property
	def controller(self):
		return sorted(
			self.ownerComp.findChildren(
				name = "videoPlayer[0-99]"),
			key = lambda operator: operator.fetch("loadTimestamp", 0)
		)
	
	@property
	def availableController(self):
		return [ controller for controller 
		  in self.controller 
		 	if controller.Idle
		]
	
	@property
	def readyController(self):
		return [ controller for controller 
		  in self.controller 
		  if controller.Ready and not controller.Running
		]
	
	@property
	def runningController(self):
		return [ controller for controller 
		  in self.controller 
		  if controller.Running
		]

	@property
	def NextUp(self):
		return [
			controller.Player.par.file.eval() for controller in self.readyController
		]

	def LoadNext(self, filepath = "", overwrite = False):
		if overwrite:
			for player in self.readyController: player.Unload()
		nextPlayer = self.availableController[0]
		self.log("Loading in to next Player", nextPlayer)
		nextPlayer.Load( filepath or self._NextFile() )
		return nextPlayer

	def _NextFile(self):
		indexPar = self.ownerComp.op("Data").par.Nextindex
		indexPar.val %= (self.ownerComp.op("playlist").numRows -1)
		indexPar.val += 1
		return self.ownerComp.op("playlist")[ indexPar, "path"].val
		return "C:/Program Files/Derivative/TouchDesigner.2023.11880/Samples/Map/Nature/Movie.1.mp4"
	
	def PlayNext(self):
		if not self.ownerComp.par.Continue.eval(): 
			self.log("Not continuing!")
			op("top_switcher").Select_Top(
				None,
				self.ownerComp.par.Transitiontime.eval()
			)	
			return
		try:
			nextPlayer = self.readyController[0]
		except IndexError:
			self.log("No ready players available, loading them in.")
			self.LoadNext()
			self.LoadNext()
			return
		self.log("Playing with Player", nextPlayer)
		nextPlayer.Start()
		self.ownerComp.op("callbackManager").Do_Callback( "onNext", nextPlayer, nextPlayer.Player, self.ownerComp )
		
	def CheckPlayNext(self):
		if len( self.runningController ): 
			self.log("Active controllers being active", self.runningController)
			return
		self.log("No players active atm, giving them a stub.")
		self.PlayNext()

	def Reset(self):
		for controller in self.controller:
			controller.Unload()
		self.ownerComp.op("callbackManager").Do_Callback( "onReset", self.ownerComp )