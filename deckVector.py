import json
from hearthstone import deckstrings
from hearthstone.enums import CardType, GameTag, Race
from collections import defaultdict
from deckWrapper import DeckWrapper
import numpy as np


from cardDB import card_db

db = card_db()
CARDCOUNT = 30






def isHighlander(myDeck):
	# need compressed list you originally get
	return len(myDeck.deck.get_dbf_id_list())==30


#Generate a vector for the manacurve of cards 0mana to 10 mana using percents
def getManaCurveVector(myDeck):
	costDict = defaultdict(int)

	for dbId in myDeck.cardList:
		card = db[int(dbId)]
		costDict[card.cost] += 1

	return [float(costDict[c]) / CARDCOUNT for c in range(0,11)]


# Generate of Vector of card type count (spells, weapons, minion, hero)
# Because EVERYTHING is a card in hearthstone, many more than this actually exists from teh games point of view
def getCardTypeVector(myDeck):
	typeDict = defaultdict(int)

	for dbId in myDeck.cardList:
		card = db[int(dbId)]
		typeDict[card.type] += 1

	return [float(typeDict[eachType]) / CARDCOUNT for eachType in CardType]


# Keywords we want to check thru, not all are relevant..
keyWords = [
	GameTag.BATTLECRY,
	GameTag.CHARGE,
	GameTag.CHOOSE_ONE,
	GameTag.COMBO,
	GameTag.CORRUPT,
	GameTag.DEATHRATTLE,
	GameTag.DISCOVER,
	GameTag.DIVINE_SHIELD,
	GameTag.FREEZE,
	GameTag.LIFESTEAL,
	GameTag.OUTCAST,
	GameTag.OVERLOAD,
	GameTag.POISONOUS,
	GameTag.SECRET,
	GameTag.SPELLPOWER,
	GameTag.SILENCE,
	GameTag.TAUNT,
	GameTag.WINDFURY,
	GameTag.RUSH,
	GameTag.TWINSPELL,
	GameTag.REBORN,
	GameTag.SPELLBURST,
]

# keywords Vector
# Generate a vector of keywords

def getKeyWordVector(myDeck):
	# no need for dictionary in this one
	kwArray = []

	for kw in keyWords:
		count = float(0)

		for dbId in myDeck.cardList:
			card = db[int(dbId)]

			# count keywords in the card
			if card.tags.get(kw, 0) or card.referenced_tags.get(kw, 0):
				count += 1

			kwArray.append(count/CARDCOUNT)

	return kwArray


