from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def testClassify(srcData, dataNeedingPrediction):
	data_train = pd.read_csv(srcData)

	data_train.head()
	data_features = data_train.copy()
	data_labels = data_features.pop('cluster')

	from sklearn import preprocessing

	le = preprocessing.LabelEncoder()

	label = data_labels


	X_train, X_test, y_train, y_test = train_test_split(data_features, label, test_size=0.2)

	knn = KNeighborsClassifier(n_neighbors=3)

	knn.fit(X_train, y_train)
	y_pred = knn.predict(X_test)
	from sklearn import metrics
	print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


