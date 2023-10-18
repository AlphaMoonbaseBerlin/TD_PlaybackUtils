'''Info Header Start
Name : extTopSwitcher
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from typing import List

class extTopSwitcher:
	"""
	extTopSwitcher description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp:COMP 	= ownerComp
		self.callback:COMP 		= self.ownerComp.op('callbackManager')
		self.standbySelectors:List[COMP] 	= []
		self.activeSelectors :List[COMP] 	= []

		self.parameterNames:List[str] = [
			"alpha", "offsetx", "offsety", "scalew", "scaleh", "rotation", "state"
		]

		for selector in self.ownerComp.findChildren( name = "selector*" ) : self._unload( selector, do_callback = False)
		
		#backwardscompatible
		self.Select_Top 	= self.SelectTop
		self.Select_Input 	= self.SelectInput

	@property
	def tweener(self) -> "COMP":
		return self.ownerComp.par.Tweener.eval()

	def _unload(self, selector:COMP, do_callback = True):
		target_top:TOP 		= selector.par.Top.eval()
		selector.par.Top.val 	= ''
		selector.par.Alpha.val 	= 0
		selector.par.State.val 	= 0
		self.standbySelectors.append( selector )
		try:
			self.activeSelectors.remove( selector )
		except:
			pass
		if do_callback: self.callback.Do_Callback( "onUnload", target_top, self.ownerComp )

	def _fadeTo(self, selector:COMP, target:str, time:float):
		for parameterName in self.parameterNames:
			self.tweener.AbsoluteTween( selector.par[ parameterName.capitalize() ], self.ownerComp.par[f"{target}{parameterName}"].eval(), time)

	def SelectTop(self, top:TOP, time:float, force:bool = False):
		if not self.standbySelectors: return
		if (not force) and (top in [selector.par.Top.eval() for selector in self.activeSelectors]): return
		for active_selector in self.activeSelectors: 
			if active_selector.par.State.eval(): self._fadeTo( active_selector, "End", time)

		selector = self.standbySelectors.pop()
		self.activeSelectors.append( selector )

		selectorTop = selector.op("video_out")
		selectorTopPath = self.ownerComp.op("comp1").relativePath( selectorTop )
		try:
			self.ownerComp.op("selectedTops").deleteRow( selectorTopPath )
		except tdError:
			pass
		self.ownerComp.op("selectedTops").appendRow( selectorTopPath )

		selector.par.Top = top
		self._fadeTo( selector, "Start", 0)
		self._fadeTo( selector, "Target", time)
		self.callback.Do_Callback( "onLoad", top, self.ownerComp )

	def SelectInput(self, index:int, time:float):
		input = self.ownerComp.op(f"input{index}")
		self.SelectTop( input, time )