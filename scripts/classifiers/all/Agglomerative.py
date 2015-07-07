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

n_clusters = int(sys.argv[1])
affinity = sys.argv[2]
linkage = sys.argv[3]
Xtr, Ytr = readXY(sys.argv[4], sys.argv[5])
Xte, Yte = readXY(sys.argv[6], sys.argv[7])
k = sys.argv[8]
if k!='all':
	k = int(k)
Xtr = normalize(Xtr, axis=0)
Xte = normalize(Xte, axis=0)
selector = SelectKBest(f_classif, k=k).fit(Xtr, Ytr)
Xtr = selector.transform(Xtr)
Xte = selector.transform(Xte)
o = open(sys.argv[9], 'w')

classifier = cluster.FeatureAgglomeration(n_clusters=n_clusters, affinity=affinity, linkage=linkage)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
