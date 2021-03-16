import numpy as np
from deckWrapper import DeckWrapper
import threading
import sys
from backports import csv
import io
import os
from updateWindow import *


def find_code(text):
    line = text.strip()
    for x in line.split(' '):
        if x.startswith('AAE'):
            return x
    return line




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




def parse_csv(filename, deckDict, classLists, window=None):
	windowUpdate=False
	if window is not None:
		windowUpdate = True
	deckDict = {}

	classLists = np.empty(10, dtype=object)
	with io.open(filename, "r", encoding = "utf-8") as csvfile:
		deckreader = list(csv.reader(csvfile, delimiter=u','))

	# get top line for Code if it exists
	schemaLine = deckreader[0]
	schema = []
	key = 0
	start = 1
	linecount = 0
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
	badLists = []
	#parse every line after schemaline
	for row in deckreader[start:]:
		if windowUpdate:
			updateTextWindow(window, "{} Teams parsed".format(linecount))
		name = row[key]
		linecount += 1
		if name not in deckDict:
			deckDict[name] = []
		#populate actual dictionary
		for index, a in enumerate(schema):

			if a!='D' or index >= len(row):
				continue
			decklist = find_code(row[index])
			deckstring= deserialize(decklist)
			nAdded = 1
			for i in range(3):
				try:
					if nAdded == 1:
						deck = DeckWrapper(name,uniqueIDCounter, (deckstring+'='*i))
						added = 0
				except Exception as e:
					continue

			#Battlefy can accept 29 card lists in some scenarios
			if len(deck.cardList) != 30:
				print("Error on {}, not 30 card list: deleting entry".format(deck.teamName))
				badLists.append(deck.teamName)
				
				continue
			else:
				deckDict[name].append(deck)
				uniqueIDCounter+=1
				if deck!=None:
					deckDict[name].append(deck)
					# add to class lists
					# ran into weird bug where some decks were double adding so check if its not already in
					if deck.ingameClass == 'demonhunter':
						if deck not in dhA:
							dhA.append(deck)
					elif deck.ingameClass == 'druid':
						if deck not in dA:
							dA.append(deck)
					elif deck.ingameClass == 'hunter':
						if deck not in hA:
							hA.append(deck)
					elif deck.ingameClass == 'mage':
						if deck not in mA:
							mA.append(deck)
					elif deck.ingameClass == 'paladin':
						if deck not in paA:
							paA.append(deck)
					elif deck.ingameClass == 'priest':
						if deck not in prA:
							prA.append(deck)
					elif deck.ingameClass == 'rogue':
						if deck not in rA:
							rA.append(deck)
					elif deck.ingameClass == 'shaman':
						if deck not in sA:
							sA.append(deck)
					elif deck.ingameClass == 'warlock':
						if deck not in wlA:
							wlA.append(deck)
					elif deck.ingameClass == 'warrior':
						if deck not in wrA:
							wrA.append(deck)
					else:
						print("Critical Error with deck parsing")
						exit(0)




	for j in badLists:
		del deckDict[j]
	classLists = np.array([dhA, dA, hA, mA, paA, prA, rA, sA, wlA, wrA], dtype=object)
	return deckDict, classLists, linecount