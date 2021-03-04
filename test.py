import numpy as np
import csvManip as csvManip
print("RUNNING TESTS\n------------------")
import pandas as pd
import os
#-------------------------------------------------
# getClusterCounts
CLASSES=["DEMONHUNTER", 'DRUID', 'HUNTER', 'MAGE', 'PALADIN', 'PRIEST', 'ROGUE', 'SHAMAN', 'WARLOCK', 'WARRIOR']
from getClusterCounts import *


#count = getClusterCounts()
#print(getClusterCounts())
assert(getClusterCounts([4,5,6,8,9,10,3,4,5,10])== [4,5,6,8,9,10,3,4,5,10]), "Error in getClusterCounts.py getClusterCounts: Preset Input Failure"
print("\n\tGetClusterCounts.py passing all tests")
#-------------------------------------------------
# DECK WRAPPER
print("\n\tStart deckWrapper.py Tests")


from deckWrapper import DeckWrapper
from typing import List

#test deck is BankYugi's warrior from "Hearthstone World Championships 2020"
deck = DeckWrapper("TeamA", 3,"AAECAQcIogKKB5uUA9+tA8XAA/bCA5PQA6rSAwtL/wOiBP8HmpQD2a0D6LADuLkDwLkD99QDtt4DAA==")

assert deck.teamName == "TeamA", "Error in deckWrapper Class with teamName"
assert deck.ingameClass == "warrior", "Error in deckWrapper Class with inGameClass"
assert deck.uID == 3, "Error in deckWrapper Class with uID"
assert deck.deckCode == "AAECAQcIogKKB5uUA9+tA8XAA/bCA5PQA6rSAwtL/wOiBP8HmpQD2a0D6LADuLkDwLkD99QDtt4DAA==", "Error in deckWrapper Class with deckCode"
testList = [75, 75, 290, 511, 511, 546, 546, 906, 1023, 1023, 51738, 51738, 51739, 55001, 55001, 55007, 55400, 55400, 56504, 56504, 56512, 56512, 57413, 57718, 59411, 59690, 60023, 60023, 61238, 61238]
assert np.array_equal(testList, deck.cardList), "error in deckWrapper Class when parsing Card List"
assert len(deck.cardList) == 30, "Error in Card Parsing"
#for i in testList:
	#assert deck.cardList[i] == testList[i], "Error in deckWrapper Class when parsing Card List"
assert deck.classification == "NoClassify", "Error in deckWrapper with Classification initialization"
#print((deck.cardList))


deck = DeckWrapper("MalfTest", 4, "AAECAZICBvIFrqsClL0C+cACws4CmdMCDEBf/gHEBuQItLsCy7wCz7wC3b4CyccCoM0Ch84CAA==")
assert deck.ingameClass == "druid", "Error in deckWrapper Class when parsing alternate hero portraits"

print("\t\tdeckWrapper Class passes all tests")

print("\tdeckWrapper.py passing all tests")

#END DECK WRAPPER
#-------------------------------------------------


#-------------------------------------------------
#START CSV MANIP
print("\n\tStart csvManip.py tests")

deckDict = {}
classLists = []
linecount = 0
filename="CSVs/tespaF2020OpenS2Finals.csv"
deckDict, classLists, linecount = csvManip.parse_csv(filename, deckDict, classLists)

assert deckDict != {}, "Error reading into Deck Dictionary"
assert deckDict["DQA into DQA"] != None, "Error when reading into deck dictionary"
assert len(classLists[0]) == 8, "error when parsing individual classes (demon Hunter)"
assert len(classLists[9]) == 5, "Error when parsing individual classes (warrior)"
print("\t\tStart Long Parse, PARALIZE THIS")
deckDict = {}
classLists = []
linecount = 0
filename = "CSVs/MTQ_IF_1to24.csv"

# THIS TAKES TOO LONG, NEEDS TO BE PARALLIZED OR SOMETHING
deckDict, classLists, linecount = csvManip.parse_csv(filename, deckDict, classLists)

#print("\t\tDH: {}".format(len(classLists[0])))
#print("\t\tDruid: {}".format(len(classLists[1])))
#print("\t\tHunter: {}".format(len(classLists[2])))
#print("\t\tMage: {}".format(len(classLists[3])))
#print("\t\tPaladin: {}".format(len(classLists[4])))
#print("\t\tPriest: {}".format(len(classLists[5])))
#print("\t\tRogue: {}".format(len(classLists[6])))
#print("\t\tShaman: {}".format(len(classLists[7])))
#print("\t\tWarlock: {}".format(len(classLists[8])))
#print("\t\tWarrior: {}".format(len(classLists[9])))

# Check Deck Count
# battlefy will old decklists containing  cards changed by the balance team that are still in the standard format, while my algorithm will mark these as invalid. This will lead to around 16 decks in Tournaments 1 to 90 submitted using invalid lists that passed their tests
# This error was discovered by manually submitting Deck Codes to a battlefy api, and my system for checking, and discovering the fault
# All cases involved players that had Identities from the Chinese servers which are not managed by Blizzard Entertainment and may be the cause
assert((len(classLists[0])+len(classLists[1])+len(classLists[2])+len(classLists[3])+len(classLists[4])+len(classLists[5])+len(classLists[6])+len(classLists[7])+len(classLists[8])+len(classLists[9])) >= (linecount*3-(linecount*3)//100)), "Error parsing decks, total count is wrong"
print("\t\tparse_csv.py Function Tests Pass")
print("\tcsvManip.py passing all tests")

#END CSV MANIP
#-------------------------------------------------


#-------------------------------------------------
#START DECK VECTOR
from deckVector import *

print("\n\tStart deckVector.py Tests")


#test deck1 has only 1 drops"
deck1 = DeckWrapper("TestDeck1", 1,"AAECAaIHApqpA6TRAw7LA8YFqJgDx5sD9acDt64Dua4Dv64DubgD0LkDqssDx84D890DgeQDAA==")

#test deck2 is half 1 drops half 2 drops
deck2 = DeckWrapper("TestDeck2", 2,"AAECAaIHBOMF7QWomAPEmAMN2AHLA90ElgaKB8ebA7euA7+uA7q4A8y5A9C5A8fOA4HkAwA=")

#test Deck3 is just a meta deck I had built ( in this case highlander priest)
deck3 = DeckWrapper("TestDeck3", 2, "AAECAZ/HAh6XAskGigf2B9MK65sDpaED/KMDmakDn6kD8qwDha0DgbEDjrEDkbEDk7oDm7oDr7oDyL4D3swDlc0DnM0Dy80D184D49ED+9ED/tED4t4D+98D+OMDAAA=")




assert(isHighlander(deck3)== True), "Failed True Highlander Parse on deckVector.py isHighlander"
assert(isHighlander(deck1)== False), "Failed False Highlander Parse on deckVector.py isHighlander"

print("\t\tisHighlander Test Pass")



assert(getManaCurveVector(deck1)==[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test Deck 1, All 1 Drop Parse on deckVector.py getManaCurveVector"
assert(getManaCurveVector(deck2)==[0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test Deck 2, Half 1 Half 2 Drop Parse on  deckVector.py getManaCurveVec"
assert(getManaCurveVector(deck3)==[0.03333333333333333, 0.16666666666666666, 0.26666666666666666, 0.26666666666666666, 0.1, 0.03333333333333333, 0.0, 0.03333333333333333, 0.03333333333333333, 0.06666666666666667, 0.0]), "Failed Test Deck 3, Highlander Priet Parse on  deckVector.py getManaCurveVector"
print("\t\tgetManaCurveVector Tests Pass")


#The game has everything in it as a card, so there are signif more slots of types than actually exist in game
assert(getCardTypeVector(deck1)==[0.0, 0.0, 0.0, 0.0, 0.36666666666666664, 0.6333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test Deck 1 on deckVector.py getCardTypeVector"
assert(getCardTypeVector(deck2)==[0.0, 0.0, 0.0, 0.0, 0.5666666666666667, 0.43333333333333335, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test Deck 1 on deckVector.py getCardTypeVector"
assert(getCardTypeVector(deck3)==[0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test Deck 1 on deckVector.py getCardTypeVector"
print("\t\tgetCardTypeVector Tests Pass")

#The game has alot of unused keywords to check thru...
assert(getKeyWordVector(deck1)== [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.1, 0.13333333333333333, 0.13333333333333333, 0.13333333333333333, 0.16666666666666666, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333,0.06666666666666667, 0.1, 0.13333333333333333, 0.16666666666666666, 0.16666666666666666, 0.16666666666666666, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.1, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667,0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), "Failed Test: deckVector.py KeywordVector Parse"
print("\t\tgetKeyWordVector Tests Pass")


assert(getClassNeutralVector(deck1) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8333333333333334, 0.0, 0.0, 0.0, 0.0, 0.16666666666666666, 0.0, 0.0]), "Failed Test Deck 1 on deckVector.py getCardNeutralVector"
assert(getClassNeutralVector(deck2) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0]), "Failed Test Deck 2 on deckVector.py getCardNeutralVector"
assert(getClassNeutralVector(deck3) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.6333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3333333333333333, 0.0, 0.0]), "Failed Test Deck 3 on deckVector.py getCardNeutralVector"
print("\t\tgetClassNeutralVector Tests Pass")

#assert(getCardSetVector(deck1) == [0.0, 0.0, 0.13333333333333333, 0.06666666666666667, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06666666666666667, 0.1, 0.2, 0.0, 0.13333333333333333, 0.0, 0.16666666666666666, 0.0, 0.0, 0.13333333333333333, 0.0]), "Failed Test Deck 1 on deckVector.py getCardSetVector"
#assert(getCardSetVector(deck2) ==[0.0, 0.0, 0.23333333333333334, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.13333333333333333, 0.0, 0.2, 0.0, 0.06666666666666667, 0.0, 0.0, 0.06666666666666667, 0.0]), "Failed Test Deck 2 on deckVector.py getCardSetVector"
#assert(getCardSetVector(deck3) == [0.0, 0.0, 0.13333333333333333, 0.03333333333333333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03333333333333333, 0.13333333333333333, 0.16666666666666666, 0.0, 0.13333333333333333, 0.0, 0.26666666666666666, 0.0, 0.0, 0.1, 0.0]), "Failed Test Deck 3 on deckVector.py getCardSetVector"
print("\t\tgetCardSetVector Tests Pass")

print("\tdeckVector.py Functions passing all tests")

#END deck Vectors
#-------------------------------------------------



#-------------------------------------------------
#START CLUSTERS
print("\n\tStart clusters.py Tests")


from clusters import *
import subprocess

def print_pretty_decks(player_class, clusters):
	#print("Printing Clusters For: %s" % player_class)
	i = 0
	L = []
	for cluster in clusters:
		#print("%s" % str(cluster))
		j = 0
		for deck in cluster.decks:
			#print("\t%s" % deck.deckCode)
			L.append(("c{}.{}".format(i,j),deck.deckCode))
			j+=1
		i+=1

	#write to CSV
	uniqueID = "{}{}".format(player_class, i)
	directName = "outputs/{}".format(player_class)
	if not os.path.exists("{}".format(directName)):
		os.mkdir("{}".format(directName))
	if not os.path.exists("{}/{}".format(directName, i)):
		os.mkdir("{}/{}".format(directName, i))
	df = pd.DataFrame(L, columns=['K', 'D'])
	df.to_csv("{}/{}/{}.csv".format(directName,i, uniqueID), encoding='utf-8', index=False, mode='w')



superCluster = -2
cluster1 = Cluster.create(Cluster, superCluster, -1, [])
assert(str(cluster1) == "Cluster Id: -1 Name: NEW"), "Test Failed clusters.py Cluster Class, string conversion"
cluster2 = Cluster.create(Cluster, superCluster, -1, [], name="TEST")
assert(str(cluster2) == "Cluster Id: -1 Name: TEST"), "Test Failed clusters.py Cluster Class, preset name"

print("\t\tCluster Class Tests Passed")


classCluster1 = ClassCluster.create(ClassCluster, superCluster, "Mage", [cluster1, cluster2])
assert(classCluster1 is not None), "Test Failed clusters.py ClassCluster Class, Error Creating Class Cluster"

print("\t\tClassCluster Class Tests Passed")



print("\t\tSuperCluster Class Tests Passed")

print("\t\tSTART CLUSTER TEST")
deckDict, classLists, linecount = csvManip.parse_csv("CSVs/MTQ_IF_1to24.csv", deckDict, classLists)
for c in classLists:
	num = 0
	for l in c:
		assert(len(l.cardList)==30), "Error at class: {} entry {}, len{}  player: {}".format(c[0].ingameClass,num, len(l.cardList), l.teamName)
		num+=1

for i in range(2, 4):
	logger.info("START SuperCluster {}".format(i))
	superCluster = createSuperCluster(classLists, clusterNumbers=getClusterCounts([40,5,7,4,8,6,7,8,9,3]))
	for class_ in CLASSES:
		aCC = superCluster.getClassClusterByName(class_)
		print_pretty_decks(class_, aCC.clusters)
	logger.info("FINISH SuperCluster {}".format(i))


#print(superCluster.chartifyData)

print("\tclusters.py Functions and Classes passing all tests")
#END CLUSTERS
#-------------------------------------------------

print("\n------------------\nALL TESTS PASSING")
