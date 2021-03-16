from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import multiprocessing
from multiprocessing.pool import Pool
from hearthstone.enums import CardClass
from deckVector import *
import os
from deckWrapper import *
from cardDB import *
import csvManip as csvManip
from itertools import repeat
from copy import deepcopy



def parseDeckInput(srcFile, deckDict, classLists, window=None):
	linecount = 0
	deckDict, classLists, linecount = csvManip.parse_csv(srcFile, deckDict, classLists, window)
	return deckDict, classLists, linecount

def testClassify(srcData, dataPoints, hero):
	if dataPoints == []:
		return []
	srcTrain = pd.read_csv(srcData)
	X=[]
	srcTrain.head()
	src_features = srcTrain.copy()
	srcs_labels = src_features.pop('cluster')

	from sklearn import preprocessing

	le = preprocessing.LabelEncoder()

	label = srcs_labels


	X_train, X_test, y_train, y_test = train_test_split(src_features, label, test_size=0.2)
	knn = KNeighborsClassifier(n_neighbors=1)

	knn.fit(src_features, srcs_labels)
	y_pred = knn.predict(X_test)
	from sklearn import metrics
	print("Accuracy:",metrics.accuracy_score(y_test, y_pred))



	
	
	
	#do the classification0
	

	Y=[]
		#if no decks do nothing
	
		#Generate Vectors to Use
	reducedSetVector = getReducedSetVector(hero=hero)
	for dp in dataPoints:

			#add all vectors for comparisons
		cards = dp.deck.cards
		cardDict = defaultdict(int)
		for (i,j) in cards:
			cardDict[i] = j
		vector = [float(cardDict[i]) / 2.0 for dbId in reducedSetVector]

		manaVector = (getManaCurveVector(dp))
		vector.extend(manaVector)


		cardTypeVector = getCardTypeVector(dp)
		vector.extend(cardTypeVector)

		keyWordVector = getKeyWordVector(dp)
		vector.extend(keyWordVector)

		classNeutralVector = getClassNeutralVector(dp)
		vector.extend(classNeutralVector)

		cardSetVector = getCardSetVector(dp)
		vector.extend(cardSetVector)

		for i in range(0,100):
			vector.append(np.array(isHighlander(dp)))

		vector = np.array(vector)

		Y.append(vector)

	Y_classified = []

	#Data into K-Means is scaled so we have to scale the data for the input here
	Y = StandardScaler().fit_transform(Y)
		#predict it
	Y_classified = knn.predict(Y)

		#reorganize results
		
	for dp, archetype in zip(dataPoints, Y_classified):
		dp.classification = archetype

	return dataPoints







