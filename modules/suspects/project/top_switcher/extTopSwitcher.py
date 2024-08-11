
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
	def selectors(self):
		return self.ownerComp.findChildren(name = "selector[1-6]", depth = 1)

	@property
	def sortedSelectors(self):
		return sorted( 
			self.selectors, 
			key = lambda selector : selector.fetch("_selectionTimestamp", 0)
		)

	@property
	def availableSelectors(self):
		return [ operator for operator in self.selectors if not operator.par.State.eval()]

	@property
	def activeSelectors(self):
		return [ operator for operator in self.selectors if operator.par.State.eval()]


	def _unload(self, selector:COMP, do_callback = True):
		target_top:TOP 		= selector.par.Top.eval()
		selector.par.Top.val 	= ''
		selector.par.Alpha.val 	= 0
		selector.par.State.val 	= 0
		if do_callback: self.callback.Do_Callback( "onUnload", target_top, self.ownerComp )

	def _fadeTo(self, selector:COMP, target:str, time:float):
		# currentStateValue 	= selector.par.State.eval()
		# targetStateVaue 	= self.ownerComp.par[f"{target}state"].eval()
		# timeAdjustment 		= abs( currentStateValue - targetStateVaue)
		timeAdjustment = 1
		for parameterName in self._absolueParameterNames:
			

			self.tweener.AbsoluteTween( 
				selector.par[ parameterName.capitalize() ], 
				self.ownerComp.par[f"{target}{parameterName}"].eval(), 
				time * timeAdjustment
			)

	def SelectTop(self, top:TOP, time:float, force:bool = False):
		for fadeOutSelector in self.activeSelectors:
			self._fadeTo( fadeOutSelector, "End", time)

		fadeInSelector = self.sortedSelectors[0]
		debug( fadeInSelector )
		fadeInSelector.par.Top = top
		fadeInSelector.store( "_selectionTimestamp", absTime.frame )
		self._fadeTo( fadeInSelector, "Start", 0)
		self._fadeTo( fadeInSelector, "Target", time)
		self.callback.Do_Callback( "onLoad", top, self.ownerComp )
		return True
	
	def SelectInput(self, index:int, time:float):
		input = self.ownerComp.op(f"input{index}")
		self.SelectTop( input, time )