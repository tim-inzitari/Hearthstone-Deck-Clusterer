#Calculate the cluster count for each class from user input
def getClusterCounts(counts=[]):
	#If i don't input counts (for testing mainly)
	if not counts:
		print("Input Cluster Counts for each Class in following format:")
		print("DH Druid Hunter Mage Paladin Priest Rogue Shaman Warlock Warrior")
		print("Example:\n1 2 3 4 5 6 7 8 9 10")
		myInputer = (input()).split()
		counts = []
		for i in myInputer:
			counts.append(int(i))

	return counts
	