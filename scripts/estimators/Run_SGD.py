import os

#Parameters:
losses = ['hinge', 'log', 'modified_huber', 'squared_hinge']
penalties = ['elasticnet']
alphas = ['0.0001', '0.001']
l1_ratios = ['0.0', '0.5', '1.0']

#Files:
trainX = '../../corpora/features.train.txt'
trainY = '../../corpora/scores.txt'
testX = '../../corpora/features.train.txt'
testY = '../../corpora/scores.txt'

#Folder name:
folder = 'sgd'
os.system('mkdir ../../scores/' + folder)

#Run all configurations in parallel:
for loss in losses:
	for penalty in penalties:
		for alpha in alphas:
			for l1_ratio in l1_ratios:
				out = '../../scores/' + folder + '/Loss=' + loss + '_Penalty=' + penalty + '_Alpha=' + alpha + '_L1Ratio=' + l1_ratio + '.txt'
				comm = 'nohup python SGD.py ' + loss + ' ' + penalty + ' ' + alpha + ' ' + l1_ratio + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
				print(comm)
				os.system(comm)
