"""Info Header Start
Name : Timeline
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End"""
import table_utils
from typing import Union

class extTimelinePlayhead:
    """
	Timeline description
	"""

    def __init__(self, ownerComp):
        self.ownerComp: Union[COMP, extTimelinePlayhead] = ownerComp
        self.playhead: Par = self.ownerComp.par.Playhead
        self._prevPlayheadValue: float = 0
        pass

    @property
    def Length(self) -> float:
        pass

    @property
    def PlayheadValue(self) -> float:
        pass

    def JumpTo(self, target: str):
        """Jump to a predefined Jumppoint."""
        pass

    def GoTo(self, target: float):
        """Jump to specific point on timeline in seconds."""
        pass

    def Continue(self):
        """If not playing, because of inactive or because of a break, continue."""
        pass

    def LeaveLoop(self):
        """If we would hit a loop the next time, continue instead."""
        pass

    def Pause(self):
        """Pause the timeline."""
        pass

    def Stop(self):
        """Completly stop the timeline."""
        pass

    def Play(self):
        """Restart the playback."""
        pass