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
fileHandler = logging.FileHandler("clustering.log")
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

