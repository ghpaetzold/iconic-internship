from sklearn import cluster
import sys, numpy, pickle
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

def writeModel(classifier, model_file):
        pickle.dump(classifier, open(model_file, "wb"))

n_clusters = int(sys.argv[1])
max_iter = int(sys.argv[2])
n_init = int(sys.argv[3])
precompute_distances = sys.argv[4]
if precompute_distances=='True':
	precompute_distances = True
if precompute_distances=='False':
	precompute_distances = False
Xtr, Ytr = readXY(sys.argv[5], sys.argv[6])
Xte, Yte = readXY(sys.argv[7], sys.argv[8])
k = sys.argv[9]
if k!='all':
	k = int(k)
Xtr = normalize(Xtr, axis=0)
Xte = normalize(Xte, axis=0)
selector = SelectKBest(f_classif, k=k).fit(Xtr, Ytr)
Xtr = selector.transform(Xtr)
Xte = selector.transform(Xte)
o = open(sys.argv[10], 'w')
model_file = sys.argv[11]

classifier = cluster.KMeans(n_clusters=n_clusters, max_iter=max_iter, n_init=n_init, precompute_distances=precompute_distances)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
writeModel(classifier, model_file)
