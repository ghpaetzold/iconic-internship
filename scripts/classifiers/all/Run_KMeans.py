import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
clusters = ['6']
iters = ['300', '500']
inits = ['10', '15']
precomputes = ['auto']
ks = ['65', 'all']
ks = ['40', '45', '50']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'kmeans'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for cluster in clusters:
		for iter in iters:
			for init in inits:
				for precompute in precomputes:
					for k in ks:
						out = tdfolder + '/NClusters=' + cluster + '_Iters=' + iter + '_NInit=' + init + '_Precompute=' + precompute + '_K=' + k + '.txt'
						comm = 'nohup python KMeans.py ' + cluster + ' ' + iter + ' ' + init + ' ' + precompute + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
						print(comm)
						os.system(comm)
