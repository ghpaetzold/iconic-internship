import sys, os, math, sys, numpy
from tabulate import tabulate

ref_file = sys.argv[1]
hyp_file = sys.argv[2]

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

#Get scores:
ref = [int(float(x.strip())) for x in open(ref_file)]
hyp = [int(float(x.strip())) for x in open(hyp_file)]

#Get accuracy measures:
sum, average, std, gravities = getScores(hyp, ref, matrix)

#Print results:
print('Results:')
print('\tSum: ' + str(sum))
print('\tAverage: ' + str(average))
print('\tStandard Deviation: ' + str(std))
print('\tGravity counts:')
for i in range(0, len(gravities)):
	print('\t\t'+str(i)+': '+str(gravities[i]))

