import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
losses = ['epsilon_insensitive', 'squared_loss', 'huber', 'squared_epsilon_insensitive']
penalties = ['elasticnet']
alphas = ['0.0001', '0.001']
l1_ratios = ['0.0', '0.5', '1.0']
ks = ['10', '20', 'all']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.scores'

#Folder name:
folder = 'sgd'
os.system('mkdir ../../../scores/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../scores/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../scores/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.scores'

	for loss in losses:
		for penalty in penalties:
			for alpha in alphas:
				for l1_ratio in l1_ratios:
					for k in ks:
						out = tdfolder + '/Loss=' + loss + '_Penalty=' + penalty + '_Alpha=' + alpha + '_L1Ratio=' + l1_ratio + '_K=' + k + '.txt'
						comm = 'nohup python SGD.py ' + loss + ' ' + penalty + ' ' + alpha + ' ' + l1_ratio + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
						print(comm)
						os.system(comm)
