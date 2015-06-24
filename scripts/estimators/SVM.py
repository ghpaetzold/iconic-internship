from sklearn import svm
import sys, numpy

def readXY(xf, yf):
	X = numpy.loadtxt(xf, delimiter='\t')
	Y = numpy.array([float(l.strip()) for l in open(xf)])
	return X, Y

def writeLabels(labels, file):
	for l in labels:
		file.write(str(l) + '\n')
	file.close()

C = float(sys.argv[1])
kernel = int(sys.argv[2])
degree = int(sys.argv[3])
gamma = float(sys.argv[4])
coef0 = float(sys.argv[5])
Xtr, Ytr = readXY(sys.argv[6], sys.argv[7])
Xte, Yte = readXY(sys.argv[8], sys.argv[9])
o = open(sys.argv[10], 'w')

classifier = svm.SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
