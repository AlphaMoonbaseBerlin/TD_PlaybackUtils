'''Info Header Start
Name : extTopSwitcher
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''



import math
class extTopSwitcher:
	"""
	extTopSwitcher description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.callback = self.ownerComp.op('callbackManager')
		self.standby_selectors = []
		self.active_selectors = []
		for selector in self.ownerComp.findChildren( name = "selector*" ) : self.Unload( selector, do_callback = False)
		self.tweenParameters = [
			"alpha", "offsetx", "offsety", "scalew", "scaleh", "rotation", "state"
		]

	@property
	def tweener(self):
		return self.ownerComp.par.Tweener.eval()

	def Unload(self, selector, do_callback = True):
		target_top = selector.par.Top.eval()
		selector.par.Top 	= ''
		selector.par.Alpha 	= 0
		selector.par.State  = 0
		self.standby_selectors.append( selector )
		try:
			self.active_selectors.remove( selector )
		except:
			pass
		if do_callback: self.callback.Do_Callback( "OnUnload", target_top )

	def fade_to(self, selector, target, time):
		for tweenParameter in self.tweenParameters:
			targetParameter = selector.par[ tweenParameter.capitalize() ]
			sourceParameter = self.ownerComp.par[f"{target}{tweenParameter}"]
			if time:
				difference = math.abs( targetParameter.eval() - sourceParameter.eval() )
				self.tweener.RelativeTween( 
						targetParameter, 
						sourceParameter.eval(), 
						time/difference)
			else:
				targetParameter = selector.par[ tweenParameter.capitalize() ]
				sourceParameter = self.ownerComp.par[f"{target}{tweenParameter}"]
				targetParameter.val = sourceParameter.eval()
			
	def Select_Top(self, top, time):
		if not self.standby_selectors: return

		for active_selector in self.active_selectors: self.fade_to( active_selector, "End", time)

		selector = self.standby_selectors.pop()
		self.active_selectors.append( selector )

		selectorTop = selector.op("video_out")
		selectorTopPath = self.ownerComp.op("comp1").relativePath( selectorTop )
		try:
			self.ownerComp.op("selectedTops").deleteRow( selectorTopPath )
		except tdError:
			pass
		self.ownerComp.op("selectedTops").appendRow( selectorTopPath )

		selector.par.Top = top
		self.fade_to( selector, "Start", 0)
		self.fade_to( selector, "Target", time)
		self.callback.Execute( "OnLoad" )( top )

	def Select_Input(self, index, time):
		input = self.ownerComp.op(f"input{index}")
		self.Select_Top( input, time )