
'''Info Header Start
Name : extTopSwitcher
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
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

		self._absolueParameterNames:List[str] = [
			"alpha", "offsetx", "offsety", "scalew", "scaleh", "rotation", "state"
		]
		
		#backwardscompatible
		self.Select_Top 	= self.SelectTop
		self.Select_Input 	= self.SelectInput

	@property
	def tweener(self) -> "COMP":
		return self.ownerComp.par.Tweener.eval()

	@property
	def availableSelectors(self):
		return [ operator for operator in self.ownerComp.findChildren(name = "selector[1-99]", depth = 1) if not operator.par.State.eval()]

	@property
	def activeSelectors(self):
		return [ operator for operator in self.ownerComp.findChildren(name = "selector[1-99]", depth = 1) if operator.par.State.eval()]


	def _unload(self, selector:COMP, do_callback = True):
		target_top:TOP 		= selector.par.Top.eval()
		selector.par.Top.val 	= ''
		selector.par.Alpha.val 	= 0
		selector.par.State.val 	= 0
		if do_callback: self.callback.Do_Callback( "onUnload", target_top, self.ownerComp )

	def _fadeTo(self, selector:COMP, target:str, time:float):

		for parameterName in self._absolueParameterNames:
			timeAdjustment = selector.par.State.eval()
			timeAdjustment = 1

			self.tweener.AbsoluteTween( 
				selector.par[ parameterName.capitalize() ], 
				self.ownerComp.par[f"{target}{parameterName}"].eval(), 
				time * timeAdjustment
			)

	def SelectTop(self, top:TOP, time:float, force:bool = False):
		for fadeOutSelector in self.activeSelectors:
			self._fadeTo( fadeOutSelector, "End", time)

		try:
			selector = self.availableSelectors.pop()
		except IndexError:
			return False

		selector.par.Top = top
		self._fadeTo( selector, "Start", 0)
		self._fadeTo( selector, "Target", time)
		self.callback.Do_Callback( "onLoad", top, self.ownerComp )
		return True
	
	def SelectInput(self, index:int, time:float):
		input = self.ownerComp.op(f"input{index}")
		self.SelectTop( input, time )