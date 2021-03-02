from hearthstone import deckstrings
from hearthstone.enums import FormatType
from typing import List, Tuple
import numpy as np
import json

from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "jsonify", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

#Hearthstone Card JSon needed for class parsing
# https://api.hearthstonejson.com/v1/latest/enUS/cards.collectible.json
cards_json = 'resources/cards.collectible.json'
card_dict = {}
with open(cards_json, encoding="utf-8") as json_file:
    data = json.load(json_file)
    for card in data:
        card_dict[card['dbfId']] = card

class DeckWrapper:


	# Constructor
	def __init__(self, teamName, uID, deckString, classification="NoClassify"):
		self.deck = deckstrings.Deck()
		self.classification = classification
		self.teamName = teamName
		self.uID = uID
		self.deckCode = deckString
		self.deck = deckstrings.Deck().from_deckstring(self.deckCode)
		self.cardList = []
		
		self.x = -1
		self.y = -1

		for cardTuple in self.deck.get_dbf_id_list():
			self.cardList.append(cardTuple[0])
			if cardTuple[1] == 2:
				self.cardList.append(cardTuple[0])

		self.ingameClass = card_dict[self.deck.heroes[0]]
		self.ingameClass = self.ingameClass['cardClass'].lower()

	def __getitem__(self, key):
		return getattr(self, key)

	def jsonify(self):
		json = {"uID": self.uID, "deckCode": self.deckCode, "classification": self.classification}
		return json
