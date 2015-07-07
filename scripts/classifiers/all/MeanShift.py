from sklearn import cluster
import sys, numpy
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

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

Xtr, Ytr = readXY(sys.argv[1], sys.argv[2])
Xte, Yte = readXY(sys.argv[3], sys.argv[4])
k = sys.argv[5]
if k!='all':
	k = int(k)
Xtr = normalize(Xtr, axis=0)
Xte = normalize(Xte, axis=0)
selector = SelectKBest(f_classif, k=k).fit(Xtr, Ytr)
Xtr = selector.transform(Xtr)
Xte = selector.transform(Xte)
o = open(sys.argv[6], 'w')

classifier = cluster.MeanShift()
classifier.fit(Xtr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
