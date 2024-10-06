'''Info Header Start
Name : extLazyVideoPlaylist
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

class extLazyVideoPlaylist:
	"""
	extLazyVideoPlaylist description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		
	@property
	def controller(self):
		return self.ownerComp.findChildren(
			name = "MoviefileIn_Controller[0-99]"
		)
	
	@property
	def freeController(self):
		return [
			controller for controller 
			in self.controller 
			if not (
				controller.Target.par.file.eval()
			)
		]
	
	@property
	def activeController(self):
		return [
			controller for controller 
			in self.controller 
			if controller.op("out1")["playing"].eval()
		]
	
	def Reset(self):
		for controller in self.controller:
			controller.Stop(reset = True)