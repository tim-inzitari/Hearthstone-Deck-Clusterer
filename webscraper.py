import requests
from bs4 import BeautifulSoup
import argparse
import io
import sys
import os
import csv

def ParseMyHtml(sourceURL, tableId, dest):

	url = sourceURL
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	final= ""
	div = soup.find('div', {"id" : tableId})
	header = ['K', 'D', 'D', 'D', 'D']
	rowlist = []
	line_count= 0
	file_path  = "{}/csv.csv".format(dest)
	with open(file_path, "a", newline='\n',encoding='utf-8') as csvfile:
		csvWriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONE)
		if os.stat(file_path).st_size == 0:
			csvWriter.writerow(['K', 'D', 'D', 'D', 'D'])
	tb = div.find('table')

	for tr in tb.find_all('tr')[2:]:
		tds = tr.find_all('td')
		#text = "{},{},{},{},{}".format(tds[1].text,tds[2].text, tds[3].text, tds[4].text, tds[5].text)
		with open(file_path, "a",newline='\n',encoding='utf-8') as csvfile:
			csvWriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
			csvWriter.writerow(["{}".format(tds[1].text),"{}".format(tds[2].text),"{}".format(tds[3].text),"{}".format(tds[4].text),"{}".format(tds[5].text)])
		#print(text)
		
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="create deck images from a csv file")
	parser.add_argument('sourceURL')
	parser.add_argument('tableId')
	parser.add_argument('dest')

	args = parser.parse_args()
	ParseMyHtml(args.sourceURL, args.tableId, args.dest)



