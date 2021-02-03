import requests, json
import argparse
import io
import sys
import os
import csv
import datetime


getTournyIDs = []
tournyIDs = []
data = requests.get("https://majestic.battlefy.com/hearthstone-masters/tournaments?start=2021-01-26T08:00:42.465Z&end=2021-02-01T08:00:42.465Z").json()
for tourny in data:
	getTournyIDs.append(tourny['_id'])
for tourny in getTournyIDs:
	data = requests.get("https://majestic.battlefy.com/tournaments/{}/".format(tourny)).json()
	tournyIDs.append(data['stageIDs'][0])
count = 1


for x in range(0, 30):
	stage = tournyIDs[x]
	tourny = getTournyIDs[x]
	print(tourny)
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

	filepath = "csv.csv"


	with open(filepath, "a", newline='\n', encoding='utf-8') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting = csv.QUOTE_NONE, escapechar='~')
		if os.stat(filepath).st_size == 0:
			csvWriter.writerow(['K', 'D', 'D', 'D', 'D'])

		for match in matches:
			data=requests.get("https://majestic.battlefy.com/tournaments/{}/matches/{}/deckstrings".format(tourny, match['_id'])).json()
			csvWriter.writerow(["{}_{}".format(count, match['top']['team']['name']).replace("\n", "").replace(",",""), "{}".format(data['top'][0]).replace("\n", "").replace(",",""), "{}".format(data['top'][1]).replace("\n", "").replace(",",""), "{}".format(data['top'][2]).replace("\n", "").replace(",","")])
			if match['isBye'] =="False":
				csvWriter.writerow(["{}_{}".format(count,match['bottom']['team']['name']).replace("\n", "").replace(",",""), "{}".format(data['bottom'][0]).replace("\n", "").replace(",",""), "{}".format(data['bottom'][1]).replace("\n", "").replace(",",""), "{}".format(data['bottom'][2]).replace("\n", "").replace(",","")])
	count +=1