import os

#Set language pair:
lang_pair = 'es-en'

#Parameters:
losses = ['epsilon_insensitive', 'squared_loss', 'huber', 'squared_epsilon_insensitive', 'hinge', 'modified_huber', 'squared_hinge']
penalties = ['elasticnet']
alphas = ['0.0001', '0.001']
l1_ratios = ['0.0', '0.5', '1.0']
ks = ['30', '40', 'all']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features_noppl'
trainY = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'sgd'
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

	for loss in losses:
		for penalty in penalties:
			for alpha in alphas:
				for l1_ratio in l1_ratios:
					for k in ks:
						out = tdfolder + '/Loss=' + loss + '_Penalty=' + penalty + '_Alpha=' + alpha + '_L1Ratio=' + l1_ratio
						out += '_K=' + k + '.txt'
						model = modelfolder + '/Loss=' + loss + '_Penalty=' + penalty + '_Alpha=' + alpha + '_L1Ratio=' + l1_ratio
						model += '_K=' + k + '.bin'
						comm = 'nohup python SGD.py ' + loss + ' ' + penalty + ' ' + alpha + ' ' + l1_ratio + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' + model + ' &'
						print(comm)
						os.system(comm)
