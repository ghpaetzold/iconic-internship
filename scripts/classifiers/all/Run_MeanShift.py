import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
ks = ['60', '65', 'all']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'meanshift'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for k in ks:
		out = tdfolder + '/K='+k+'.txt'
		comm = 'nohup python MeanShift.py ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
		print(comm)
		os.system(comm)
