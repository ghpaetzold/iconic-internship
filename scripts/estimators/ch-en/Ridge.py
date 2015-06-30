from sklearn import linear_model
import sys, numpy
from sklearn.preprocessing import normalize

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

normalize = True
if sys.argv[1].strip()!='True':
	normalize = False
solver = sys.argv[2]
Xtr, Ytr = readXY(sys.argv[3], sys.argv[4])
Xte, Yte = readXY(sys.argv[5], sys.argv[6])
o = open(sys.argv[7], 'w')

classifier = linear_model.Ridge(normalize=normalize, solver=solver)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
