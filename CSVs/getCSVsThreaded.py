import requests, json
import argparse
import io
import sys
import os
import csv
import datetime
import multiprocessing
from multiprocessing.pool import Pool
from itertools import product


NUM_PROCESSSES = 20
START_DATE = "2021-01-16" #YYYY-MM-DD
END_DATE = "2021-02-18"#YYYY-MM-DD

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
	data = requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, matches[4]['_id'])).json()
	#print(data['top'][1])
	


	myString= ""
	for match in matches:
		data=requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, match['_id'])).json()
		myString+="\n{},".format(tourny)+"{}_{}".format(count+1, match['top']['team']['name']).replace("\n", "").replace(",","") + ","+"{}".format(data['top'][0]).replace("\n", "").replace(",","")+","+ "{}".format(data['top'][1]).replace("\n", "").replace(",","")+","+"{}".format(data['top'][2]).replace("\n", "").replace(",","")
		if match['isBye'] =="False":
			myString+="\n{},".format(tourny)+"{}_{}".format(count+1, match['bottom']['team']['name']).replace("\n", "").replace(",","") + ","+"{}".format(data['bottom'][0]).replace("\n", "").replace(",","")+","+ "{}".format(data['bottom'][1]).replace("\n", "").replace(",","")+","+"{}".format(data['bottom'][2]).replace("\n", "").replace(",","")

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
    main()