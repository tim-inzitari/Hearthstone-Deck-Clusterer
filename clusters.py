import json
from hearthstone.enums import CardClass
from copy import deepcopy #we want new values not reference values on copy
from datetime import date
import matplotlib.pyplot as plt
import csv
from deckVector import *
from deckWrapper import *
from cardDB import *
from getClusterCounts import *
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from tfKMeans import *

global CLUSTER_NUMBERS
CLASSES=["DEMONHUNTER", 'DRUID', 'HUNTER', 'MAGE', 'PALADIN', 'PRIEST', 'ROGUE', 'SHAMAN', 'WARLOCK', 'WARRIOR']
db = card_db()




#Clustering process wants a more precise log for debug purposes
# Copied from example at @ https://docs.python.org/3/howto/logging.html
import logging

#create logger

logging.basicConfig(
     level=logging.INFO, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
formatter = logging.Formatter('%(levelname)s %(asctime)s:\t %(message)s', 
                    datefmt='%m/%d/%Y%I:%M:%S %p')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

console.setFormatter(formatter)




logger = logging.getLogger('clustering')

logger.info("START NEW\n--------------------------------------------------------------------------")





"""
cluster of decks

"""
class Cluster:
	

	# Initializer, defines no Factory style to use
	def __init__(self, *args, **kwargs):
		self._factory = None
		self._superCluster = None

	#Function to Create New Cluster with variable Factory function
	@staticmethod
	def create(factory, superCluster, clusterID, decks, name="NEW"):
		self = factory()
		self._factor = factory
		self._superCluster = superCluster
		self.clusterID = clusterID
		self.decks = decks or []
		self.name = name

		#initialize decks to this cluster
		self._initializeDecks()

		return self

	#Assign each deck to this cluster on creation
	def _initializeDecks(self):
		for deck in self.decks:
			deck.clusterID = self.clusterID
			deck.classification = self.name



	def __str__(self):
		clustID = self.clusterID
		clustName = self.name


		return("Cluster Id: {} Name: {}".format(clustID, clustName))



	def __repr__(self):
		return str(self)

	def updateNames(self):
		for deck in self.decks:
			#print(self.name)
			deck.classification = "{} {}".format(self.name, deck.ingameClass)
			#print(deck.classification)

# Collection of clusters sorted by class
class ClassCluster:

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._factory = None
		self._superCluster = None

	#create function
	@staticmethod
	def create(factory, superCluster, inGameClass, clusters):
		self = factory()
		self._factory = factory
		self._superCluster = superCluster

		self.inGameClass = inGameClass
		self.clusters = clusters

		return self


	#string conversion
	def __str__(self):
		return "{} Set, contains {} clusters".format(self.inGameClass, len(self.clusters))

	def __repr__(self):
		return str(self)


	@property
	def getInGameClass(self):
		return CardClass(self.inGameClass).name


	# Function to convert to a dictionary for input usage
	def convertToDict(self):
		for cluster in self.clusters:
			yield(cluster.clusterID, cluster.decks)


#Collection of ClassClusters
#Used to save a configuration for later Classification
class SuperCluster:
	CLASS_FACTORY = ClassCluster
	CLUSTER_FACTORY = Cluster
	

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._factory = None

	def __str__(self):
		result = "Cluster Set: "
		myCCs = self.myClassClusters

		for classCluster in myCCs:
			result += "\n{}".format(str(classCluster))
		return result


	def __repr__(self):
		return str(self)


	def getClassClusterByName(self, gameClassName):
		myClass = int(CardClass[gameClassName])
		#print(myClass)
		#print(self.myClassClusters)
		for cc in self.myClassClusters:
			#print(cc.getInGameClass)
			if cc.inGameClass == myClass:
				return cc
		print("FAIL")


		# Function to convert to a dictionary for input usage
	def convertToDict(self):
		for classCluster in self.myClassClusters:
			yield(classCluster.inGameClass, classCluster.clusters)



	#for TSNE displays might delete later
	def chartifyData(self, theDateUpdated=""):
		result = []


		for aCC in self.myClassClusters:
			myXs = []
			myYs = []
			myLabels = []
			clusters= {}
			for cluster in aCC.clusters:
				if cluster.clusterID not in clusters:
					clusters[cluster.clusterID] = []
				for dp in cluster.decks:
					myXs.append(dp["x"])
					myYs.append(dp["y"])
					myLabels.append(dp.clusterID)
					
					clusters[cluster.clusterID].append(tuple((dp["x"], dp["y"])))
			#print(clusters)
			for c in clusters:
				first = [t[0] for t in clusters[c]]
				second = [t[1] for t in clusters[c]]
				plt.scatter(first, second)

			plt.title(CardClass(aCC.inGameClass).name)
			plt.ylabel("y")
			plt.xlabel("x")
			plt.show()
			result.append(tuple((myXs, myYs, myLabels)))



		
		return result

from updateWindow import *
def createSuperCluster(inData, scFact=SuperCluster, clusterNumbers=[3,3,3,3,3,3,3,3,3,3], window=None):
	from sklearn import manifold
	from sklearn.cluster import KMeans
	from sklearn.preprocessing import StandardScaler

	windowUpdate = True
	if window == None:
		windowUpdate=False

	superCluster = scFact()
	superCluster._factory= scFact

	# deep copy because we need new instances
	data = deepcopy(inData)
	clusterCountMover = 0;
	classClusters = []
	CLUSTER_NUMBERS = clusterNumbers

	for hero, dataPoints in zip(CLASSES, data):
		logger.info("Start Clustering for: {}".format(hero))
		X = []
		if windowUpdate:
			updateTextWindow(window, "Clustering {} Decks".format(hero))
			#fix weird bug where DH is only class not displaying
			if hero == "DEMONHUNTER":
				updateTextWindow(window, "Clustering DH Decks".format(hero))


		#Generate Vectors used in Classifications

		reducedSetVector = getReducedSetVector(hero=hero)
		logger.info("Base Cluster Length: %s" % len(reducedSetVector))


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

			#We want highlander to be very important so it gets more than one spot
			

			X.append(vector)
			if hero == "MAGE":
				#print(vector)
				if len(vector) != 2018:
					print(dp.teamName)
				#print(len(vector))
		#print(X)
		X = np.array(X, dtype=float)

		logger.info("Full Feature Vector Length: %s" % len(X[0]))

		#Do Machine Learning

		X = StandardScaler().fit_transform(X)
		#print(X.shape)
		#labels = KmeansTF(X, CLUSTER_NUMBERS[clusterCountMover])
		print("")
		
		myClusterMaker = KMeans(n_clusters=min(CLUSTER_NUMBERS[clusterCountMover], len(X)))
		myClusterMaker.fit(X)
		labels = myClusterMaker.labels_

		#myClusterMaker.fit(X)
		if windowUpdate:
			updateTextWindow(window, "Labeling {} decks".format(hero))
			#fix weird bug where DH is only class not displaying
			if hero == "DEMONHUNTER":
				updateTextWindow(window, "Labeling DH Decks".format(hero))
		
		
		if not os.path.exists("outputs/labels/NEW_labels"):
			os.mkdir("outputs/labels/NEW_labels")
		df = pd.DataFrame(X)
		df["cluster"]= labels
		df = df.sort_values("cluster")

		df.to_csv("outputs/labels/NEW_labels/{}_labels.csv".format(hero), mode="w+", encoding='utf-8', index=False)


		dpsInCluster = defaultdict(list)
		for dp, cID in zip(dataPoints, labels):#myClusterMaker.labels_):
			dpsInCluster[int(cID)].append(dp)

		clusters = []
		for id, dataPointIter in dpsInCluster.items():
			clusters.append(Cluster.create(superCluster.CLUSTER_FACTORY, superCluster, id, dataPointIter))
		#print(len(clusters)
		#print(type(clusters))
		classCluster = ClassCluster.create(superCluster.CLASS_FACTORY, superCluster, int(CardClass[hero]), clusters)
		classClusters.append(classCluster)
		clusterCountMover +=1


		logger.info("END Clustering for: {}\n\n".format(hero))
	superCluster.myClassClusters = classClusters



	return superCluster


