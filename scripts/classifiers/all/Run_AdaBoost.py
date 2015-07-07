import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
n_estimators = ['50', '75']
learning_rates = ['1', '0.1']
algorithms = ['SAMME', 'SAMME.R']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'adaboost'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for n_estimator in n_estimators:
		for learning_rate in learning_rates:
			for algorithm in algorithms:
				out = tdfolder + '/Estimators=' + n_estimator + '_LearningRate=' + learning_rate + '_Algorithm=' + algorithm + '.txt'
				comm = 'nohup python AdaBoost.py ' + n_estimator + ' ' + learning_rate + ' ' + algorithm + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
				print(comm)
				os.system(comm)
