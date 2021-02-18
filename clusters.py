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
	def _augment_data_points(self):
		for deck in self.decks:
			deck.clusterID = self.clusterID
			deck.classification = self.name


	#String Casting
	#def __str__(self):
