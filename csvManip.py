import numpy as np
from deckWrapper import DeckWrapper

from backports import csv
import io
import os







def deserialize(input):
	deck = None
	lines = input.split('\n')
	deckString = None;

	for line in lines:
		if line is None:
			continue
		if line.startswith("#"):
			#Pastebin copies remove newlines so we gotta do this
			if line.find("#AAE") != -1:
				# Account for deck named AAE
				if line.find("#AAE") == line.find("###AAE"): 
					line = line[line.find("###AAE"+6):]
				start = line.find("AAE")
				line = line[start:]
				end = line.find("#")
				line = line[:end]
				return line
			continue
		if deckString is None:
			deckString = line
			return deckString
	return None


# Class Code for List Vector:
# Demon Hunter = 0
# Druid = 1 
# Hunter = 2
# Mage = 3
# Paladin = 4
# Priest = 5
# Rogue = 6
# Shaman = 7
# Warlock = 8
# Warrior = 9

def parse_csv(filename, deckDict, classLists):

	deckDict = {}
	classLists = np.empty(10, dtype=np.object)
	with io.open(filename, "r", encoding = "utf-8") as csvfile:
		deckreader = list(csv.reader(csvfile, delimiter=u','))

	# get top line for Code if it exists
	schemaLine = deckreader[0]
	schema = []
	key = 0
	start = 1
	uniqueIDCounter = 0
	deckstring = ""

	dhA,dA,hA,mA,paA,prA,rA,sA,wlA,wrA = [],[],[],[],[],[],[],[],[],[]


	for index, x in enumerate(schemaLine):
		if x=='D':
			schema.append('D')
		elif x=='K':
			schema.append('K')
			key = index
		else:
			schema.append('')


	# if no schema make it Key followed by decks
	if not any(schema):
		schema = ['K']
		for i in range(len(schemaLine)-1):
			schema.append('D')
		start-=1

	#parse every line after schemaline
	for row in deckreader[start:]:
		name = row[key]

		if name not in deckDict:
			deckDict[name] = []

		for index, a in enumerate(schema):
			if a!='D' or index >= len(row):
				continue
			deckstring= deserialize(row[index])
			for i in range(3):
				try:
					deck = DeckWrapper(name,uniqueIDCounter, (deckstring+'='*i))
					uniqueIDCounter+=1
					if deck!=None:
						deck_dict[name].append(deck)

						# add to class lists
						if deck.ingameClass == 'demonhunter':
							dhA.append(deck)
						elif deck.ingameClass == 'druid':
							dA.append(deck)
						elif deck.ingameClass == 'hunter':
							hA.append(deck)
						elif deck.ingameClass == 'mage':
							mA.append(deck)
						elif deck.ingameClass == 'paladin':
							paA.append(deck)
						elif deck.ingameClass == 'priest':
							prA.append(deck)
						elif deck.ingameClass == 'rogue':
							rA.append(deck)
						elif deck.ingameClass == 'shaman':
							sA.append(deck)
						elif deck.ingameClass == 'warlock':
							wlA.append(deck)
						elif deck.ingameClass == 'warrior':
							wrA.append(deck)
						else:
							print("Critical Error with deck parsing")
							exit(0)
				except Exception as e:
					continue

		classLists = np.array([dhA, dA, hA, mA, paA, prA, rA, sA, wlA, wrA], dtype=np.object)

