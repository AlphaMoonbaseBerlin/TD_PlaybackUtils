'''Info Header Start
Name : extAudioOneshot
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.35320
Info Header End'''

from pathlib import Path
from TDStoreTools import StorageManager
import TDFunctions as TDF

class extAudioOneshot:
	"""
	extAudioOneshot description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp:COMP = ownerComp
		
	
	def newPlayer(self, filepath):
		newPlayer = self.ownerComp.copy( self.ownerComp.op("prefab"), name = "player0")
		newPlayer.nodeX = self.ownerComp.op("prefab").nodeX + 300
		newPlayer.nodeY = 200 * newPlayer.digits
		newPlayer.par.Audiofile.val = filepath
		newPlayer.tags.add("Removeable")
		return newPlayer
	
	def Clear(self):
		for item in self.ownerComp.findChildren( depth = 1, tags = ["Removeable"]):
			item.destroy()
	
	def Play(self, filepath:Path, channels):
		filepath = Path( filepath )
		if not filepath.is_file(): return 
		
		availablePlayer = [ player for player in self.ownerComp.findChildren(
			depth = 1, type = baseCOMP, parName = "Audiofile"
		) if player.par.Inactive.eval() and player.par.Audiofile.val == str(filepath) ]  or [ self.newPlayer(filepath) ]
		#
		
		nextPlayer = availablePlayer.pop()
		
		nextPlayer.par.Channels.val = channels
		nextPlayer.par.Cuepulse.pulse()