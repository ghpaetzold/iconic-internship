from sklearn.preprocessing import MinMaxScaler
import sys, os

def readX(xf):
        X = []
        for line in open(xf):
                values = [float(v) for v in line.strip().split('\t')]
                X.append(values)
        return X

def writeX(x, out):
	o = open(out, 'w')
	for i in range(0, len(x)):
		line = ''
		for value in x[i]:
			line += str(value) + '\t'
		o.write(line.strip() + '\n')
	o.close()

langs = os.listdir('/export/data/ghpaetzold/iconicinternship/python/corpora/')
langs = [lang for lang in langs if '-' in lang]

for lang in langs:
	print(str(lang))
	files = os.listdir('/export/data/ghpaetzold/iconicinternship/python/corpora/'+lang+'/features/')
	basepath = '/export/data/ghpaetzold/iconicinternship/python/corpora/'+lang+'/features/'
	for file in files:
		print('\t'+str(file))
		X = readX(basepath+file)
		scaler = MinMaxScaler()
		X = scaler.fit_transform(X)
		writeX(X, basepath+file+'_norm')
