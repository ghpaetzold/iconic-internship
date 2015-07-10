from sklearn import linear_model
import sys, numpy
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn import tree
from sklearn import ensemble

def readXY(xf, yf):
	X = []
	for line in open(xf):
		values = [float(v) for v in line.strip().split('\t')]
		X.append(values)
	Y = numpy.array([float(l.strip()) for l in open(yf)])
	return X, Y

def writeLabels(labels, file):
	c = -1
	for l in labels:
		c += 1
		file.write(str(l) + '\n')
	file.close()

n_estimators = int(sys.argv[1])
learning_rate = float(sys.argv[2])
algorithm = sys.argv[3]
Xtr, Ytr = readXY(sys.argv[4], sys.argv[5])
Xte, Yte = readXY(sys.argv[6], sys.argv[7])
o = open(sys.argv[8], 'w')

classifier = ensemble.AdaBoostClassifier(n_estimators=n_estimators, learning_rate=learning_rate, algorithm=algorithm)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
