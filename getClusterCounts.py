#Calculate the cluster count for each class 
def getClusterCounts(counts=[]):
	#If i don't input counts (for testing mainly)
	if not counts:
		print("Input Cluster Counts for each Class in following format:")
		print("DH Druid Hunter Mage Paladin Priest Rogue Shaman Warlock Warrior")
		print("Example:\n1 2 3 4 5 6 7 8 9 10")
		dh, d, h, m, pa, pr, r, s, l, w = int(input().split())
		counts = [dh, d, h, m ,pa, pr, r, s, l, w]

	return counts
	