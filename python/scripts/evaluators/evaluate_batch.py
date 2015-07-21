import sys, os, math, sys, numpy
from tabulate import tabulate

lang_pair = sys.argv[1]

def getScores(hyp, ref, matrix):
	try:
		gravities = [0, 0, 0, 0]
		values = []
		for i in range(0, len(hyp)):
			gravity = matrix[hyp[i]][ref[i]]
			gravities[gravity] += 1
			values.append(float(gravity))		
		values = numpy.array(values)
		return numpy.sum(values), numpy.average(values), numpy.std(values), gravities
	except Exception:
		return 999999, 999999, 999999, [999999, 999999, 999999, 999999]

#Get evaluation matrix:
matrix = []
matrix.append([0,0,0,1,2,2])
matrix.append([0,0,0,1,2,2])
matrix.append([0,0,0,0,2,2])
matrix.append([1,1,0,0,0,2])
matrix.append([3,3,3,0,0,0])
matrix.append([3,3,3,3,0,0])

#Get main folder:
mainfolder = '../../classes/'+lang_pair+'/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get datasets:
datasets = os.listdir(mainfolder+mlfolders[0])

#Create total map:
totalmap = {}

for dataset in datasets:
	print('For test set: ' + dataset)

	table = []
	headers = ['Method', 'Sum', 'Average', 'Std', 'Counts', 'Model']

	#Get reference TER scores:
	ref = [int(float(x.strip())) for x in open('../../corpora/'+lang_pair+'/datasets/'+dataset+'_test.classes')]
	
	#Get scores:
	for mlfolder in mlfolders:
		minvalues = (9999999999, 999999, 99999, 999999)
		minfile = ''
		files = []
		try:
			files = os.listdir(mainfolder + mlfolder + '/' + dataset + '/')
		except Exception:
			pass
		for file in files:
			hyp = [int(float(x.strip())) for x in open(mainfolder + mlfolder + '/' + dataset + '/' + file)]
			if len(ref)==len(hyp):
				sum, average, std, gravities = getScores(hyp, ref, matrix)
				if sum<minvalues[0]:
					minvalues = (sum, average, std, gravities)
					minfile = file
		table.append([mlfolder, minvalues[0], "%.3f" % minvalues[1], "%.3f" % minvalues[2], minvalues[3], minfile])

		if mlfolder not in totalmap.keys():
			totalmap[mlfolder] = [minvalues[0], minvalues[1], minvalues[2], minvalues[3][0], minvalues[3][1], minvalues[3][2], minvalues[3][3]]
		else:
			totalmap[mlfolder][0] += minvalues[0]
			totalmap[mlfolder][1] += minvalues[1]
			totalmap[mlfolder][2] += minvalues[2]
			totalmap[mlfolder][3] += minvalues[3][0]
			totalmap[mlfolder][4] += minvalues[3][1]
			totalmap[mlfolder][5] += minvalues[3][2]
			totalmap[mlfolder][6] += minvalues[3][3]
	print(tabulate(table, headers=headers) + '\n')

folders = ['kmeans', 'decisiontree', 'randomforest', 'svm', 'sgd']
for folder in folders:
	data = totalmap[folder]
	sum = str(data[0])
	avg = str("%.3f" % data[1])
	std = str("%.3f" % data[2])
	scores = str([data[3], data[4], data[5], data[6]])
	print(sum + '|||' + avg + '|||' + std + '|||' + scores)
