'''Info Header Start
Name : Timeline
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
import table_utils
from typing import Union

class extTimelinePlayhead:
	"""
	Timeline description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp:Union[COMP, extTimelinePlayhead] = ownerComp
		self.playhead:Par = self.ownerComp.par.Playhead
		self._prevPlayheadValue:float = 0
		self.ownerComp.op('Emitter').Attach_Emitter( self )

	@property
	def Length(self) -> float:
		return self.ownerComp.par.Length.eval()

	@property
	def PlayheadValue(self) -> float:
		return self.ownerComp.par.Playhead.eval()

	def _updatePlayhead(self):
		if not self.ownerComp.par.Active.eval() or self.ownerComp.par.Pause.eval(): return
		self._prevPlayheadValue = self.playhead.eval()
		self.playhead.val += absTime.stepSeconds
		self._validatePlayhead()

	def JumpTo(self, target:str):
		"""Jump to a predefined Jumppoint."""
		cell:Cell = self.ownerComp.op("jumppoint_repo").Repo[ target, "point"]
		if not cell: return
		self.GoTo( float( cell.val ))

	def GoTo(self, target:float):
		"""Jump to specific point on timeline in seconds."""
		self.playhead.val = target
		#self.Continue()
		self.LeaveLoop()
		self._validatePlayhead()
		self.Emit("GoTo", target)

	def _validatePlayhead(self):
		self._checkLoopRegion()
		self._checkBreakpoint() 
		if self.ownerComp.par.Loop.eval():
			self.playhead.val %= self.Length
		else:
			self.playhead.val = tdu.clamp(self.playhead.eval(), 0, self.Length)

	def _checkLoopRegion(self):
		regions = table_utils.table_to_dict( self.ownerComp.op("loop_repo").Repo )
		inLoopRegion = False
		for region in regions:
			if ( self.PlayheadValue < float(region["end"]) and self.PlayheadValue > float(region["start"]) ): inLoopRegion = True
			if  not( self.PlayheadValue > float(region["end"]) and self._prevPlayheadValue <= float(region["end"]) ): continue
			
			
			region_length = float( region["end"]) - float( region["start"] )
			new_position = ((self.PlayheadValue - float( region["start"] )) % region_length) +float( region["start"] )

			if not self.ownerComp.par.Leaveloopregion.eval(): self.playhead.val = new_position
			else: self.ownerComp.par.Leaveloopregion.val = False
		self.ownerComp.par.Inloopregion.val = inLoopRegion
		
	def _checkBreakpoint(self):
		breakpoints = table_utils.table_to_dict( self.ownerComp.op("breakpoint_repo").Repo )
		for region in breakpoints:
			if  not( self.PlayheadValue >= float(region["point"]) and self._prevPlayheadValue < float(region["point"]) ): continue
			self.Pause()


	def Continue(self):
		"""If not playing, because of inactive or because of a break, continue."""
		self.ownerComp.par.Pause = False
		self.ownerComp.par.Active = True

	def LeaveLoop(self):
		"""If we would hit a loop the next time, continue instead."""
		self.ownerComp.par.Leaveloopregion = True

	def Pause(self):
		"""Pause the timeline."""
		self.ownerComp.par.Pause.val = True
		self.Emit("Break")

	def Stop(self):
		"""Completly stop the timeline."""
		self.Emit("Stop")
		self.ownerComp.par.Active = False

	def Play(self):
		"""Restart the playback."""
		self.Emit("Play")
		self.Continue()