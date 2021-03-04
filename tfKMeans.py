import tensorflow as tf
import numpy as np



#Define a function to get closest centroids for KMeans implementation
def closest_centroids(points, centroids, vectorLength):
	distances = tf.reduce_sum(tf.math.squared_difference(points, centroids[:,None]), 2)
	assignments = tf.argmin(distances, axis=0)
	#print("hello")
	return assignments

#Define a function for Kmeans Implementation to move centroids based on sum of squared distances
def move_centroids(points, closest, centroids):
	new_centroids = []
	for k in range(centroids.shape[0]):
		#print(np.array(points[np.array(closest==k)]).shape)
		if np.array(points[np.array(closest==k)]).shape[0] == 0:
		#	print("1 decker")
			#if empty cluster retry in middle
			new_centroids.append(np.nanmean(np.array(points), axis=0))
		
			#continue
		else:
			new_centroids.append(np.nanmean(points[np.array(closest==k)], axis=0))
	return np.array(new_centroids)



#Kmeans Implementation using TensorFlow 2.0
#taken from packet book and modified
def KmeansTF(X, cluster_n):
	#Get Data Entries and Vector length from Numpy Array Shape
	dataCount, vectorLength = X.shape
	#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
	#tf.convert_to_tensor(X, dtype=tf.float64)
	#print(X)
	#a = np.savetxt("test.csv", X, delimiter=',')
	#print(X.shape)
	zeroes = []
	for i in range(0,vectorLength):
		zeroes.append(0.0)
	print(X)

	#Start by selecting 3 random points
	centroids = tf.slice(tf.random.shuffle(X), [0,0], [cluster_n, -1])
	print(centroids.shape)

	#Define Variable to detect if movement happens
	movementOccurred = True
	closest = []
	#Continue algorithm until no movement
	stepCount = 0
	while movementOccurred:
		past_centroids = centroids
		closest = closest_centroids(X, centroids, vectorLength)
		centroids = move_centroids(X, closest, centroids)

		# use equal function t
		#for i in tf.reduce_sum(tf.square(np.subtract(centroids, past_centroids)), axis=1):
			#if i != 0:
				#print(i)
			#	i = i
		if np.array_equiv(centroids[:cluster_n], past_centroids[:cluster_n]):
			movementOccurred = False
			print("DONE")
		stepCount+=1
		del past_centroids
		#exit after 10000 epochs no matter waht
		if stepCount == 10000:
			movementOccurred= False
		#print("EPOCH: {}".format(stepCount))
	print(centroids)
	print("{} epochs".format(stepCount))
	return(closest)
