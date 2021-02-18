import json
from hearthstone.enums import CardClass
from copy import deepcopy #we want new values not reference values on copy



from deckVector import *
from deckWrapper import *
from cardDB import *
from getClusterCounts import *



db = card_db()
CLUSTER_NUMBERS = getClusterCounts([3,3,3,3,3,3,3,3,3,3])


#Clustering process wants a more precise log for debug purposes
# Copied from example at @ https://docs.python.org/3/howto/logging.html
import logging

#create logger
logger = logging.getLogger('clustering')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s %(asctime)s:\t %(message)s', 
                    datefmt='%m/%d/%Y%I:%M:%S %p')

fileHandler = logging.FileHandler("clustering.log", 'w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)

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