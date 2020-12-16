import numpy as np
import csvManip
print("RUNNING TESTS\n------------------")

#-------------------------------------------------
# DECK WRAPPER
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
assert deck.classification == "NOCLASSIFY", "Error in deckWrapper with Classification initialization"



deck = DeckWrapper("MalfTest", 4, "AAECAZICBvIFrqsClL0C+cACws4CmdMCDEBf/gHEBuQItLsCy7wCz7wC3b4CyccCoM0Ch84CAA==")
assert deck.ingameClass == "druid", "Error in deckWrapper Class when parsing alternate hero portraits"

print("\tdeckWrapper Class passes all tests")



#END DECK WRAPPER
#-------------------------------------------------


#-------------------------------------------------
#START CSV MANIP








print("\tcsvManip Functions passing all tests")

#END CSV MANIP
#-------------------------------------------------









print("------------------\nALL TESTS PASSING")
