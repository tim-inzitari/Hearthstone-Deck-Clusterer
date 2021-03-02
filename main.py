#import SimpleGUI Framework to use in the project 
import PySimpleGUI as sg
from deckWrapper import DeckWrapper
from typing import List
import pandas as pd
import numpy as np
import csvManip as csvManip
import os
from cardDB import *
from clusters import *
import subprocess
from tkinter import *
import json
import random
from copy import deepcopy #we want new values not reference 


CLASSES=["DEMONHUNTER", 'DRUID', 'HUNTER', 'MAGE', 'PALADIN', 'PRIEST', 'ROGUE', 'SHAMAN', 'WARLOCK', 'WARRIOR']



def getNRandomItems(myList, n):
	return random.sample(myList, n)

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

# Main process
if __name__== "__main__":
	#add the layout start
	cluster_counts = []
	filename=""

	#layout for first page
	layout = [[sg.Text("Welcome To Deck Clusterer Tool!")],
			[sg.Text("Enter integer Cluster Counts for Each Class in form")],
			[sg.Text("DH"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Druid"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Hunter"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Mage"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Paladin"), sg.InputText('1', size=(5,1),  enable_events=True)],
			[sg.Text("Priest"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Rogue"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Shaman"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Warlock"), sg.InputText('1', size=(5,1),  enable_events=True), sg.Text("Warrior"), sg.InputText('1', size=(5,1),  enable_events=True)],
			[sg.Text("Input CSV"), sg.InputText(size=(50,1), enable_events=True, key="-FILE-"), sg.FileBrowse(file_types=(("CSVs","*.csv"),))],
			[sg.Text("Output:"), sg.Text(size=(40,1), key='-OUTPUT-')],
			[sg.Text("")],
			[sg.Text("Next will start parsing the CSV, this may take some time")],
			[sg.Button('Next', bind_return_key=True), sg.Button('Cancel')]]


	#create teh window
	window = sg.Window("Deck Cluster Tool", layout)
	myOutput = ""
	#Event Loop to Gather Inputs for Cluster Count
	#event loop to process "events" that get "values" of inputs
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': 
		# if user closes window or clicks cancel
			window.close()
			quit()
		# if next is clicked go next
		if event == "Next":
			cluster_counts = []
			for i in range(0,10):
				cluster_counts.append(int(values[i]))
			break



		# Get File name
	#	if event == "-FILE-":
	#		filename= values["-FILE-"]

		#parse Cluster Counts
		cluster_counts = []
		myOutput = ""
		for i in range(0,10):
			myOutput += (" {}".format(values[i]))
			
		window['-OUTPUT-'].update(myOutput)
	



	window.close()


	# DEBUG ONLY
	#filename = "CSVs/MTQ_IF_1to24.csv"


	# Parse CSV

	deckDict = {}
	classLists = []
	linecount = 0
	deckDict, classLists, linecount = csvManip.parse_csv(filename, deckDict, classLists)

	deckCount = 0
	for i in classLists:
		deckCount+= len(i)


	#make next window
	layout=[ [sg.Text("Stage 2 Deck Parsing Complete!!")],
			 [sg.Text("Total Teams: {}".format(linecount)), sg.Text("Total Valid Decks: {}, Class Totals Below".format(deckCount))],
			 [sg.Text("DH: {}, Druid: {}, Hunter: {}, Mage: {}, Paladin: {}".format(len(classLists[0]), len(classLists[1]), len(classLists[2]), len(classLists[3]), len(classLists[4])))],
			 [sg.Text("Priest: {}, Rogue: {}, Shaman: {}, Warlock: {}, Warrior: {}".format(len(classLists[5]), len(classLists[6]), len(classLists[7]), len(classLists[8]), len(classLists[9])))],
			 [sg.Text("")],
			 [sg.Text("Press Next to Start Clustering, This may take some time")],
			 [sg.Button('Next', bind_return_key=True), sg.Button('Cancel')]
			 												]

	window = sg.Window("Deck Cluster Tool", layout)

	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': 
		# if user closes window or clicks cancel
			window.close()
			break
		# if next is clicked go next
		if event == "Next":
			break
		
	window.close()



#Start Clustering Phase

	
	superCluster = createSuperCluster(classLists, clusterNumbers=cluster_counts)

	#Get Layout
	layout=[ [sg.Text("Stage 3 Deck Clustering Complete!!")],
			 [sg.Text("")],
			 [sg.Text("Press Next to Start Naming Clusters")],
			 [sg.Button('Next', bind_return_key=True), sg.Button('Cancel')]]

	window = sg.Window("Deck Cluster Tool", layout)
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': 
		# if user closes window or clicks cancel
			window.close()
			break
		if event == "Next":
			break
	window.close()



	L=[]
	#Generate frames to view sample decks
	#First we must generate a selection of decks to display
	for class_ in CLASSES:
		count = 0
		aCC = superCluster.getClassClusterByName(class_)
		for cluster in aCC.clusters:
			if len(cluster.decks) <= 3:
				# Case for each so we always have 3 decks in csv
				if len(cluster.decks) == 3:
					L.append(("{} {}".format(class_,count), cluster.decks[0].deckCode, cluster.decks[1].deckCode, cluster.decks[2].deckCode))
				if len(cluster.decks) == 2:
					L.append(("{} {}".format(class_,count), cluster.decks[0].deckCode, cluster.decks[1].deckCode, ""))
				if len(cluster.decks) == 1:
					L.append(("{} {}".format(class_,count), cluster.decks[0].deckCode, "", ""))
			else:
				#Randomly Select 3 to display
				randomSelection = getNRandomItems(cluster.decks, 3)
				L.append(("{} {}".format(class_,count), randomSelection[0].deckCode, randomSelection[1].deckCode, randomSelection[2].deckCode))
			count += 1

	#Convert that to a CSV File
	df = pd.DataFrame(L, columns=['K','D','D','D'])
	df.to_csv("outputs/tmp/tmp.csv", encoding = 'utf-8', index=False, mode='w')

	#run decktoImagePNG so we have images to display
	cmd = "python decktoImagePNG.py deckcsv outputs/tmp/tmp.csv outputs/tmp"
	os.system(cmd)

	for class_ in CLASSES:
		#define layout to display


		#acctually display
		i=0
		aCC = superCluster.getClassClusterByName(class_)
		for cluster in aCC.clusters:
			imageColumn = [ 
						[sg.Image(key="-IMAGE-", filename="outputs/tmp/{} {}.png".format(class_, i))]
		]
			textColumn = [	[sg.Text("Stage 4 Declaring Names on {}".format(class_))],
							[sg.Text("Next to Continue to Next Deck/Class/Stage")],
							[sg.Text("Decks in Cluster: {}".format(len(cluster.decks)))],
							[sg.Text("Define this Deck: "), sg.InputText("".format(class_), key="-INPUT-")],
					 		[sg.Button('Next', bind_return_key=True), sg.Button('Cancel')]]
			layout = [ 
						[sg.Column(textColumn), sg.VSeparator(), sg.Column(imageColumn, scrollable=True, size=(800,800))]
					 ]
			window = sg.Window("Cluster Classification", layout, size=(1200,800))
			
			while True:
				event, values = window.read()

				if event == sg.WIN_CLOSED or event == 'Cancel': 
					# if user closes window or clicks cancel
					window.close()
					break
				#Classify the category and continue
				if event == "Next":
					cluster.name = values["-INPUT-"]
					break
			window.close()
			#print(cluster)
			i+=1
			layout=[]

			#update every deck in the cluster to its new name
			cluster.updateNames()
	#End Stage 4

	#Export results and finish
	layout=[ [sg.Text("Stage 4 Deck Classification Complete!!")],
			[sg.Text("")],
			 [sg.Text("Press Next to Start Stage 5: Data Export")],
			 [sg.Button('Next', bind_return_key=True), sg.Button('Cancel')]]
	window = sg.Window("Deck Cluster Tool", layout)
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel': 
		# if user closes window or clicks cancel
			window.close()
			break
		if event == "Next":
			break
	window.close()

	#CSV Write of Archetypes
	outputList = []
	outputDeckDict = {}

	#remake deck dictionary for output
	for class_ in CLASSES:
		aCC = superCluster.getClassClusterByName(class_)
		for cluster in aCC.clusters:
			for deck in cluster.decks:
				if deck.teamName not in outputDeckDict:
					outputDeckDict[deck.teamName] = []
				outputDeckDict[deck.teamName].append(deepcopy(deck))


	for name in outputDeckDict:
		subList = []
		subList.append(name)
		for deck in outputDeckDict[name]:
			subList.append(deck.classification)
		outputList.append(subList)
	
	df_out = pd.DataFrame(outputList)
	df_out.to_csv("outputs/outputCSV/{}_archetypes.csv".format(os.path.splitext(os.path.basename(filename))[0]), encoding='utf-8', index=False, mode='w')

	#Make Json of SuperCluster

	
	with open('outputs/saved_superClusters/{}_cluster.json'.format(os.path.splitext(os.path.basename(filename))[0]), 'w+') as outfile:
		json.dump(superCluster.jsonify(), outfile)


#end main