import json
from hearthstone.enums import CardClass
from copy import deepcopy #we want new values not reference values on copy
from datetime import date
import matplotlib.pyplot as plt

from deckVector import *
from deckWrapper import *
from cardDB import *
from getClusterCounts import *


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
A collection of Decks that have similar gameplans and similar cards

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


	#convert to json for an output
	def jsonify(self):
		json = {"clusterID": self.clusterID, "name": self.name, "decks": self.decks} 
		return json


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

	# Send to json for an output
	def jsonify(self):
		result = {"inGameClass": self.getInGameClass, "clusters": []}
		for cluster in self.clusters:
			result["clusters"].append(cluster.jsonify())

		return result


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


	def jsonify(self):
		result= {"Date": date.today().strftime("%B %d, %Y"), "classClusters": []}

		for cc in self.myClassClusters:
			result["classClusters"].append(cc.jsonify())

		return json.dumps(result, indent=4)


	def chartifyData(self, theDateUpdated=""):
		result = []

		for hero, clusters in self.items():
			heroResult = {"inGameClass": CardClass(int(hero)).name, "data": [], "clustMap": {}, "clustNames": {}, "dateUpdated": theDateUpdated}

			for clust in clusters:
				heroResult["clustMap"][c.clusterID] =c.clusterID


				for datapoint in clust.decks:
					archetypeName = datapoint.classification
					clusterID = int(data_point.clusterID)

					metadata = {"clusterName": archetypeName, "clusterID": clusterID, "deckList":datapoint.cardList}

					heroResult["data"].append({"x": datapoint["x"], "y": datapoint["y"], "metadata": metadata})
			result.append(heroResult)

		return result



def createSuperCluster(inData, scFact=SuperCluster, clusterNumbers=[3,3,3,3,3,3,3,3,3,3]):
	from sklearn import manifold
	from sklearn.cluster import KMeans
	from sklearn.preprocessing import StandardScaler

	

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

			vector.append(isHighlander(dp))

			cardTypeVector = getCardTypeVector(dp)
			vector.extend(cardTypeVector)

			keyWordVector = getKeyWordVector(dp)
			vector.extend(keyWordVector)

			classNeutralVector = getClassNeutralVector(dp)
			vector.extend(classNeutralVector)

			cardSetVector = getCardSetVector(dp)
			vector.extend(cardSetVector)

			X.append(vector)

		logger.info("Full Feature Vector Length: %s" % len(X[0]))
		#do machine learning
		# Use TSNE to help visualize the high dimensonal data
		if len(dataPoints) > 1:
			tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
			xy = tsne.fit_transform(deepcopy(X))
			for (x,y), dp in zip(xy, dataPoints):
				dp.x = float(x)
				dp.y = float(y)
		elif len(dataPoints) == 1:
				#in case of only one deck just dump it at origin
			dataPoints[0].x = 0.0
			dataPoints[0].y = 0.0
		else:
				#Nothing here
			continue


		X = StandardScaler().fit_transform(X)
		myClusterMaker = KMeans(n_clusters=min(CLUSTER_NUMBERS[clusterCountMover], len(X)))

		

		myClusterMaker.fit(X)

		dpsInCluster = defaultdict(list)
		for dp, cID in zip(dataPoints, myClusterMaker.labels_):
			dpsInCluster[int(cID)].append(dp)

		clusters = []
		for id, dataPointIter in dpsInCluster.items():
			clusters.append(Cluster.create(superCluster.CLUSTER_FACTORY, superCluster, id, dataPointIter))
		#print(len(clusters))
		#print(type(clusters))
		classCluster = ClassCluster.create(superCluster.CLASS_FACTORY, superCluster, int(CardClass[hero]), clusters)
		classClusters.append(classCluster)
		clusterCountMover +=1
		logger.info("END Clustering for: {}\n\n".format(hero))
	superCluster.myClassClusters = classClusters



	return superCluster

