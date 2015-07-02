from sklearn.metrics import *
import sys, os

#Get main folder:
mainfolder = '../../../scores/ch-en/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get datasets:
datasets = os.listdir(mainfolder+mlfolders[0])

for dataset in datasets:
	print('For dataset: ' + dataset)

	#Get reference TER scores:
	ref = [float(x) for x in open('../../../corpora/ch-en/datasets/'+dataset+'_test.scores')]
	
	#Get scores:
	for mlfolder in mlfolders:
		minmse = 999999999
		minmae = 999999999
		minfile = ''
		files = []
		try:
			files = os.listdir(mainfolder + mlfolder + '/' + dataset + '/')
		except Exception:
			pass
		for file in files:
			hyp = [float(x) for x in open(mainfolder + mlfolder + '/' + dataset + '/' + file)]
			if len(ref)==len(hyp):
				mse = mean_squared_error(ref, hyp)
				mae = mean_absolute_error(ref, hyp)
				if mse<minmse:
					minmse = mse
					minmae = mae
					minfile = file
		print('\tFor ' + mlfolder + ': ' + str(minmse) + '/' + str(minmae) + ': ' + minfile)
