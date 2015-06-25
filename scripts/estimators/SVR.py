from sklearn import svm
import sys, numpy

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

C = float(sys.argv[1])
epsilon = float(sys.argv[2])
kernel = sys.argv[3]
degree = int(sys.argv[4])
gamma = float(sys.argv[5])
coef0 = float(sys.argv[6])
Xtr, Ytr = readXY(sys.argv[7], sys.argv[8])
Xte, Yte = readXY(sys.argv[9], sys.argv[10])
o = open(sys.argv[11], 'w')

classifier = svm.SVR(C=C, epsilon=epsilon, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
