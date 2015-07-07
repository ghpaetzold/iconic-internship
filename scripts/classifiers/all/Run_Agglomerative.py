import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
clusters = ['6']
affs = ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']
links = ['ward', 'complete', 'average']
ks = ['65', 'all']
#ks = ['40', '45', '50']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'agglomerative'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for cluster in clusters:
		for aff in affs:
			for link in links:
				for k in ks:
					out = tdfolder + '/NClusters=' + cluster + '_Affinity=' + aff + '_Linkage=' + link + '_K=' + k + '.txt'
					comm = 'nohup python Agglomerative.py ' + cluster + ' ' + aff + ' ' + link + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
					print(comm)
					os.system(comm)
