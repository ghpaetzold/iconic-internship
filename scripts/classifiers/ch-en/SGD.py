from sklearn import linear_model
import sys, numpy
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression

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

loss = sys.argv[1]
penalty = sys.argv[2]
alpha = float(sys.argv[3])
l1_ratio = float(sys.argv[4])
Xtr, Ytr = readXY(sys.argv[5], sys.argv[6])
Xte, Yte = readXY(sys.argv[7], sys.argv[8])
k = sys.argv[9]
if k!='all':
	k = int(k)
Xtr = normalize(Xtr, axis=0)
Xte = normalize(Xte, axis=0)
Xtr = SelectKBest(f_regression, k=k).fit_transform(Xtr, Ytr)
Xte = SelectKBest(f_regression, k=k).fit_transform(Xte, Yte)
o = open(sys.argv[10], 'w')

classifier = linear_model.SGDClassifier(loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
