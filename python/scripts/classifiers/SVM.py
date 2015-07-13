from sklearn import svm
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

C = float(sys.argv[1])
kernel = sys.argv[2]
degree = int(sys.argv[3])
gamma = float(sys.argv[4])
coef0 = float(sys.argv[5])
Xtr, Ytr = readXY(sys.argv[6], sys.argv[7])
Xte, Yte = readXY(sys.argv[8], sys.argv[9])
Xtr = normalize(Xtr, axis=0)
Xte = normalize(Xte, axis=0)
k = sys.argv[10]
if k!='all':
        k = int(k)
selector = SelectKBest(f_classif, k=k).fit(Xtr, Ytr)
Xtr = selector.transform(Xtr)
Xte = selector.transform(Xte)
o = open(sys.argv[11], 'w')
model_file = sys.argv[12]

classifier = svm.SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
writeModel(classifier, model_file)
