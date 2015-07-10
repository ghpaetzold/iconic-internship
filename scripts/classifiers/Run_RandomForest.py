import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
n_estimators = ['50', '75']
criterions = ['gini', 'entropy']
max_features = ['sqrt', 'log2', 'None']
max_depths = ['3', '5', 'None']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features_noppl'
trainY = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'randomforest'
os.system('mkdir ../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../corpora/'+lang_pair+'/features/'+td+'_test.features_noppl'
        testY = '../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for n_estimator in n_estimators:
		for criterion in criterions:
			for max_feature in max_features:
				for max_depth in max_depths:
					out = tdfolder + '/Estimators=' + n_estimator + '_Criterion=' + criterion + '_MaxFeat=' + max_feature + '_MaxDepth=' + max_depth + '.txt'
					comm = 'nohup python RandomForest.py ' + n_estimator + ' ' + criterion + ' ' + max_feature + ' ' + max_depth + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
					print(comm)
					os.system(comm)
