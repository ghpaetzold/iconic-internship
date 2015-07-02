import sys, os, math

def getDistScores(hyp, ref):
	result = {}
	for i in range(0, 6):
		result[i] = 0
	for i in range(0, len(hyp)):
		diff = math.fabs(hyp[i]-ref[i])
		result[diff] += 1
	return result

#Get main folder:
mainfolder = '../../../classes/ch-en/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get datasets:
datasets = os.listdir(mainfolder+mlfolders[0])

for dataset in datasets:
	print('For dataset: ' + dataset)

	#Get reference TER scores:
	ref = [float(x.strip()) for x in open('../../../corpora/ch-en/datasets/'+dataset+'_test.classes')]
	
	#Get scores:
	for mlfolder in mlfolders:
		maxdist = -1
		maxd = None
		maxfile = ''
		files = []
		try:
			files = os.listdir(mainfolder + mlfolder + '/' + dataset + '/')
		except Exception:
			pass
		for file in files:
			hyp = [float(x.strip()) for x in open(mainfolder + mlfolder + '/' + dataset + '/' + file)]
			if len(ref)==len(hyp):
				dists = getDistScores(hyp, ref)
				if dists[0]>maxdist:
					maxdist = dists[0]
					maxd = dists
					maxfile = file
		print('\tFor ' + mlfolder + ': ' + str(maxdist) + '/' + str(maxd) + ': ' + maxfile)
