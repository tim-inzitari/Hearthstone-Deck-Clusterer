print("RUNNING TESTS")



# DECK WRAPPER
from deckWrapper import DeckWrapper

deck = DeckWrapper("TeamA", 1, 3,"AAECAR8eqAK1A8cDhwSKB9sJ/gz8owOmpQP5rgP7rwP8rwOHsAOiuQOkuQP/ugPXvgPevgPczAOizgOC0APG0QO50gP21gPo4QPy4QOE4gOG4gOP4wPK4wMAAA==")

assert deck.teamName == "TeamA", "Error in deckWrapper Class with teamName"
assert deck.ingameClass == 1, "Error in deckWrapper Class with inGameClass"
assert deck.uID == 3, "Error in deckWrapper Class with uID"
assert deck.deckCode == "AAECAR8eqAK1A8cDhwSKB9sJ/gz8owOmpQP5rgP7rwP8rwOHsAOiuQOkuQP/ugPXvgPevgPczAOizgOC0APG0QO50gP21gPo4QPy4QOE4gOG4gOP4wPK4wMAAA==", "Error in deckWrapper Class with deckCode"
assert deck.cardList == [(296, 1), (437, 1), (455, 1), (519, 1), (906, 1), (1243, 1), (1662, 1), (53756, 1), (53926, 1), (55161, 1), (55291, 1), (55292, 1), (55303, 1), (56482, 1), (56484, 1), (56703, 1), (57175, 1), (57182, 1), (58972, 1), (59170, 1), (59394, 1), (59590, 1), (59705, 1), (60278, 1), (61672, 1), (61682, 1), (61700, 1), (61702, 1), (61839, 1), (61898, 1)], "Error in deckWrapper Class when parsing Card List"
assert deck.classification == "NOCLASSIFY", "Error in deckWrapper with Classification initialization"

print("\tdeckWrapper Class passes all tests")

#END DECK WRAPPER



