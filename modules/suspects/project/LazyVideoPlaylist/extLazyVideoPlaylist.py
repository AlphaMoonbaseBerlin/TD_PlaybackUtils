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
		  if not controller.op("out1")["open"].eval()
		  and not controller.op("out1")["opening"].eval()
		]
	
	@property
	def readyController(self):
		return [ controller for controller 
		  in self.controller 
		  if controller.op("out1")["open"].eval()
		  and not controller.op("out1")["playing"].eval()
		]
	
	@property
	def runningController(self):
		return [ controller for controller 
		  in self.controller 
		  if controller.op("out1")["playing"].eval()
		  and not controller.op("out1")["trigger"].eval()
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
		try:
			nextPlayer = self.readyController[0]
		except IndexError:
			self.log("No ready players available, loading them in.")
			self.LoadNext()
			self.LoadNext()
			return
		self.log("Playing with Player", nextPlayer)
		nextPlayer.Start()
		self.ownerComp.op("callbackManager").Do_Callback( "onNext", nextPlayer, nextPlayer.Player )
		op("top_switcher").Select_Top(
			nextPlayer.op("video_out"),
			self.ownerComp.par.Transitiontime.eval()
		)

	def CheckPlayNext(self):
		if len( self.runningController ): return
		self.log("No players active atm, giving them a stub.")
		self.PlayNext()

	def Reset(self):
		for controller in self.controller:
			controller.Unload()
		self.ownerComp.op("top_switcher").Select_Top(None, 0)