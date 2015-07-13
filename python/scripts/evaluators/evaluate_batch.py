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
					minvalues = (sum, "%.3f" % average, "%.3f" % std, gravities)
					minfile = file
		table.append([mlfolder, minvalues[0], minvalues[1], minvalues[2], minvalues[3], minfile])

	print(tabulate(table, headers=headers) + '\n')
