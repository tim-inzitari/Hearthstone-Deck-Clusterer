from hearthstone import deckstrings
from hearthstone.enums import FormatType
from typing import List, Tuple
import numpy as np

class DeckWrapper:

	# Constructor
	def __init__(self, teamName, ingameClass, uID, deckString):
		self.deck = deckstrings.Deck()

		self.teamName = teamName
		self.ingameClass = ingameClass
		self.uID = uID
		self.deckCode = deckString
		self.deck = deckstrings.Deck().from_deckstring(self.deckCode)
		self.cardList = []
		self.classification = "NOCLASSIFY"

		for cardTuple in self.deck.get_dbf_id_list():
			self.cardList.append(cardTuple[0])
			if cardTuple[1] == 2:
				self.cardList.append(cardTuple[0])
		self.cardList = np.array(self.cardList)