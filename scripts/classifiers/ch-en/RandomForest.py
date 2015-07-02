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
criterion = sys.argv[2]
max_features = sys.argv[3]
if max_features=="None":
        max_features = None
max_depth = sys.argv[4]
if max_depth=="None":
        max_depth = None
else:
        max_depth = int(max_depth)
Xtr, Ytr = readXY(sys.argv[5], sys.argv[6])
Xte, Yte = readXY(sys.argv[7], sys.argv[8])
#Xtr = normalize(Xtr, axis=0)
#Xte = normalize(Xte, axis=0)
o = open(sys.argv[9], 'w')

classifier = ensemble.RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_features=max_features, max_depth=max_depth)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
