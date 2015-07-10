import sys, os, math, sys

lang_pair = sys.argv[1]

def getScores(hyp, ref, matrix):
	try:
		gravities = [0, 0, 0, 0]
		score = 0
		for i in range(0, len(hyp)):
			gravity = matrix[hyp[i]][ref[i]]
			gravities[gravity] += 1
			score += gravity
		return gravities, score
	except Exception:
		return [999999, 999999, 999999, 999999], 99999

#Get evaluation matrix:
matrix = []
matrix.append([0,0,0,1,2,2])
matrix.append([0,0,0,1,2,2])
matrix.append([0,0,0,0,2,2])
matrix.append([1,1,0,0,0,2])
matrix.append([3,3,3,0,0,0])
matrix.append([3,3,3,3,0,0])
print(str(matrix[5][0]))

#Get main folder:
mainfolder = '../../../classes/'+lang_pair+'/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get datasets:
datasets = os.listdir(mainfolder+mlfolders[0])

for dataset in datasets:
	print('For dataset: ' + dataset)

	#Get reference TER scores:
	ref = [int(float(x.strip())) for x in open('../../../corpora/'+lang_pair+'/datasets/'+dataset+'_test.classes')]
	
	#Get scores:
	for mlfolder in mlfolders:
		minscore = 9999999999999
		ming = None
		minfile = ''
		files = []
		try:
			files = os.listdir(mainfolder + mlfolder + '/' + dataset + '/')
		except Exception:
			pass
		for file in files:
			hyp = [int(float(x.strip())) for x in open(mainfolder + mlfolder + '/' + dataset + '/' + file)]
			if len(ref)==len(hyp):
				gravities, score = getScores(hyp, ref, matrix)
				if score<minscore:
					minscore = score
					ming = gravities
					minfile = file
		print('\tFor ' + mlfolder + ': ' + str(minscore) + '/' + str(ming) + ': ' + minfile)
