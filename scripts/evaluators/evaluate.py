from sklearn.metrics import *
import sys, os

#Get main folder:
mainfolder = '../../scores/'

#Get ML techniques:
mlfolders = os.listdir(mainfolder)

#Get reference TER scores:
ref = [float(x) for x in open('../../corpora/scores.txt')]

#Get scores:
for mlfolder in mlfolders:
	minmse = 999999999
	minmae = 999999999
	files = os.listdir(mainfolder + mlfolder + '/')
	for file in files:
		hyp = [float(x) for x in open(mainfolder + mlfolder + '/' + file)]
		if len(ref)==len(hyp):
			mse = mean_squared_error(ref, hyp)
			mae = mean_absolute_error(ref, hyp)
			if mse<minmse:
				minmse = mse
				minmae = mae
	print('For ' + mlfolder + ': ' + str(minmse) + '/' + str(minmae))
