from hearthstone import deckstrings
from hearthstone.enums import FormatType

class DeckWrapper:

	# Constructor
	def __init__(self, teamName, ingameClass, uID, deckString):
		self.deck = deckstrings.Deck()

		self.teamName = teamName
		self.ingameClass = ingameClass
		self.uID = uID
		self.deckCode = deckString
		self.deck = deckstrings.Deck().from_deckstring(self.deckCode)
		self.cardList = self.deck.get_dbf_id_list()
