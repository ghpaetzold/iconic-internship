import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
norms = ['True', 'False']
solvers = ['svd', 'cholesky', 'lsqr', 'sparse_cg']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.scores'

#Folder name:
folder = 'ridge'
os.system('mkdir ../../../scores/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../scores/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../scores/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.scores'

	for norm in norms:
		for solver in solvers:
			out = tdfolder + '/Norm=' + norm + '_Solver=' + solver + '.txt'
			comm = 'nohup python Ridge.py ' + norm + ' ' + solver + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
			print(comm)
			os.system(comm)
