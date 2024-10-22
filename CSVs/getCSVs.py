import requests, json
import argparse
import io
import sys
import argparse
import os
import csv
import datetime as dt
from datetime import datetime

import multiprocessing
from multiprocessing.pool import Pool
from itertools import product


NUM_PROCESSSES = multiprocessing.cpu_count()
global START_DATE #YYYY-MM-DD
global END_DATE#YYYY-MM-DD

def parseTournament(stage, tourny, count):
	print("Start tourny {} id: {}".format(count+1, tourny))
	data= requests.get("https://dtmwra1jsgyb0.cloudfront.net/stages/{}/matches?roundNumber=1".format(stage)).json()
	#print(type(data))
	#print(type(data[3]))

	#print(data[0]['_id'])

	matches = []

	for match in data:
		#print(match['_id'])
		matches.append(match)

	#print(matches)
	#data = requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, matches[4]['_id'])).json()
	#print(data['bottom'][1])
	#print("\n")
	

	#parse r1
	myString= ""
	for match in matches:
		data=requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, match['_id'])).json()
		if (len(data['top']) != 0):
			myString+="\n{},".format(tourny)+"{}_{}".format(count+1, match['top']['team']['name']).replace("\n", "").replace(",","")
			for i in range(len(data['top'])):
				myString+=","+"{}".format(data['top'][i]).replace("\n","").replace(",","")
		#","+"{}".format(data['top'][0]).replace("\n", "").replace(",","")+","+ "{}".format(data['top'][1]).replace("\n", "").replace(",","")+","+"{}".format(data['top'][2]).replace("\n", "").replace(",","")
		if match['isBye'] == False:
			if (len(data['bottom']) != 0):
				myString+="\n{},".format(tourny)+"{}_{}".format(count+1, match['bottom']['team']['name']).replace("\n", "").replace(",","")# + ","+"{}".format(data['bottom'][0]).replace("\n", "").replace(",","")+","+ "{}".format(data['bottom'][1]).replace("\n", "").replace(",","")+","+"{}".format(data['bottom'][2]).replace("\n", "").replace(",","")
				for i in range(len(data['bottom'])):
					myString+=","+"{}".format(data['bottom'][i]).replace("\n","").replace(",","")

	print("End Tourny {}".format(count+1))
	return myString

#	with open(filepath, "a", newline='\n', encoding='utf-8') as csvfile:
	#	csvWriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting = csv.QUOTE_NONE, escapechar='~')
	#	if os.stat(filepath).st_size == 0:
			#csvWriter.writerow(['K', 'D', 'D', 'D', 'D'])

		#for match in matches:
			#data=requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, match['_id'])).json()
			#csvWriter.writerow(["{}_{}".format(count, match['top']['team']['name']).replace("\n", "").replace(",",""), "{}".format(data['top'][0]).replace("\n", "").replace(",",""), "{}".format(data['top'][1]).replace("\n", "").replace(",",""), "{}".format(data['top'][2]).replace("\n", "").replace(",","")])
			#if match['isBye'] =="False":
			#	csvWriter.writerow(["{}_{}".format(count,match['bottom']['team']['name']).replace("\n", "").replace(",",""), "{}".format(data['bottom'][0]).replace("\n", "").replace(",",""), "{}".format(data['bottom'][1]).replace("\n", "").replace(",",""), "{}".format(data['bottom'][2]).replace("\n", "").replace(",","")])


def main():
	getTournyIDs = []
	tournyIDs = []
	data = requests.get("https://majestic.battlefy.com/hearthstone-masters/tournaments?start={}T08:00:42.465Z&end={}T08:00:42.465Z".format(START_DATE, END_DATE)).json()
	for tourny in data:
		getTournyIDs.append(tourny['_id'])
	num_tourneys = len(getTournyIDs)
	for tourny in getTournyIDs:
		data = requests.get("https://majestic.battlefy.com/tournaments/{}/".format(tourny)).json()
		tournyIDs.append(data['stageIDs'][0])
	filepath = "csv.csv"
	print("Parsing {} tournaments using up to {} processes.".format(num_tourneys, NUM_PROCESSSES))
	p = Pool(processes = NUM_PROCESSSES)
	returnData = p.starmap(parseTournament, zip(tournyIDs, getTournyIDs, range(num_tourneys)))
	p.close()
	p.join()


	print("Parsing Complete\nStart CSV file write:")
	with open(filepath, "a", newline='\n', encoding='utf-8') as csvfile:
		if os.stat(filepath).st_size == 0:
			csvfile.write(",K,D,D,D") #TournyID, Name, Deck, Deck, Deck
		for processString in returnData:
			split = processString.split(",")
			for line in split:
				csvfile.write("{}".format(line))
				csvfile.write(",")
			

	print("Finish CSV File Write")
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Get Start and End Date")
	parser.add_argument("startDate", help="STARTDATE format: YYYY-MM-DD-hh-mm-ss Note, 24 hour time UCT Timezone")
	parser.add_argument("endDate", help="ENDDATE format: MM-DD-YYYY-hh-mm-ss Note, 24 hour time UCT Timezone")
	args = parser.parse_args()
	START_DATE = args.startDate	
	END_DATE = args.endDate	
	main()