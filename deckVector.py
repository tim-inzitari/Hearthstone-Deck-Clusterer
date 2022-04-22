import json
from hearthstone import deckstrings
from hearthstone.enums import CardType, GameTag, CardClass, CardSet
from collections import defaultdict
from deckWrapper import DeckWrapper
import numpy as np


from cardDB import card_db

db = card_db()
CARDCOUNT = 30





# Check if the deck is Highlander (no duplicate cards)
def isHighlander(myDeck):
	# need compressed list you originally get
	if len(myDeck.deck.get_dbf_id_list())==30:
		return float(1)
	else:
		return float(0)


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
	GameTag.FRENZY,
	GameTag.TRADEABLE,
	GameTag.COLOSSAL,
	GameTag.DREDGE,
	GameTag.TAG_ONE_TURN_EFFECT,
	GameTag.QUESTLINE,
	GameTag.RITUAL,
	GameTag.TOPDECK,
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

			kwArray.append(float(count/CARDCOUNT))

	return kwArray


#Generate a vector for how many cards are Class cards vs Neutral Cards
def getClassNeutralVector(myDeck):

	clNeutDict = defaultdict(int)

	for dbId in myDeck.cardList:
		card = db[int(dbId)]

		clNeutDict[card.card_class]+=1

	return [float(clNeutDict[cClass])/CARDCOUNT for cClass in CardClass]



# Generate a Vector for how many cards are from each set
def getCardSetVector(myDeck):

	setVector = defaultdict(int)

	for dbId in myDeck.cardList:
		card = db[int(dbId)]

		setVector[card.card_set] +=1

	return [float(setVector[s])/CARDCOUNT for s in CardSet]


def getReducedSetVector(hero=None):
	if hero:
		heroes = (CardClass[hero], CardClass.NEUTRAL)
		allCards = [c for c in db.values() if c.collectible and c.card_class in heroes]
	else:
		allCards = [c for c in db.values() if c.collectible]

	return [c.dbf_id for c in sorted(allCards, key=lambda c: c.dbf_id)]
