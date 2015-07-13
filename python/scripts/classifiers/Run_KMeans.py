import os

#Set language pair:
lang_pair = 'es-en'

#Parameters:
clusters = ['6']
iters = ['300', '500']
inits = ['10', '15']
precomputes = ['auto']
ks = ['40', 'all']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features_noppl'
trainY = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'kmeans'
os.system('mkdir ../../classes/'+lang_pair)
os.system('mkdir ../../models/'+lang_pair)
os.system('mkdir ../../classes/'+lang_pair+'/'+folder)
os.system('mkdir ../../models/'+lang_pair+'/'+folder)
os.system('mkdir ../../models/'+lang_pair+'/'+folder+'/'+trainDataset)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../classes/'+lang_pair+'/'+folder+'/'+td
	modelfolder = '../../models/'+lang_pair+'/'+folder+'/'+trainDataset

        testX = '../../corpora/'+lang_pair+'/features/'+td+'_test.features_noppl'
        testY = '../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for cluster in clusters:
		for iter in iters:
			for init in inits:
				for precompute in precomputes:
					for k in ks:
						out = tdfolder + '/NClusters=' + cluster + '_Iters=' + iter + '_NInit=' + init
						out += '_Precompute=' + precompute + '_K=' + k + '.txt'
						model = modelfolder + '/NClusters=' + cluster + '_Iters=' + iter + '_NInit=' + init
						model += '_Precompute=' + precompute + '_K=' + k + '.txt'
						comm = 'nohup python KMeans.py ' + cluster + ' ' + iter + ' ' + init + ' ' + precompute + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' + model + ' &'
						print(comm)
						os.system(comm)
