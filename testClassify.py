from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
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
from sklearn import svm
from sklearn.neural_network import MLPClassifier

import matplotlib.pyplot as plt  
from sklearn.metrics import plot_confusion_matrix
import matplotlib
import math
matplotlib.interactive(True)
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

	displayLabels = []
	label = srcs_labels
	for s in srcs_labels:
		if s != hero:
			displayLabels.append(s.split()[0])
	srcs_labels = displayLabels
	label = srcs_labels
	input_size = src_features.shape[1]
	#print("ADAM, {} 250 500".format(math.floor(input_size/2.0)))
	#print("ADAM 64 48")
	print("SVM")
	X_train, X_test, y_train, y_test = train_test_split(src_features, label, test_size=0.2, random_state=0)
	#model = KNeighborsClassifier(n_neighbors=11, p=1)
	model = svm.SVC(random_state=0, C=1.0)
	model.fit(src_features, srcs_labels)

	#model = MLPClassifier(random_state=0, max_iter=50000, hidden_layer_sizes=(64,48), early_stopping=True, solver='adam', warm_start=True)


	y_pred = model.predict(X_test)
	from sklearn import metrics
	print("{} Accuracy:".format(hero),metrics.accuracy_score(y_test, y_pred))
	#plot_confusion_matrix(model, X_test, y_test)
	#plt.title(hero)
	#plt.show()



	
	
	
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

	Y = np.array(Y, dtype=float)
	Y_classified = []

	#Data into K-Means is scaled so we have to scale the data for the input here
	Y = StandardScaler().fit_transform(Y)
		#predict it
	Y_classified = model.predict(Y)

		#reorganize results
		
	for dp, archetype in zip(dataPoints, Y_classified):
		dp.classification = archetype

	return dataPoints







