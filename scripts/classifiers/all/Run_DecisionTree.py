import os

#Set language pair:
lang_pair = 'en-es'

#Parameters:
criterions = ['gini', 'entropy']
splitters = ['best', 'random']
max_features = ['sqrt', 'log2', 'None']
max_depths = ['3', '5', 'None']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'decisiontree'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	for criterion in criterions:
		for splitter in splitters:
			for max_feature in max_features:
				for max_depth in max_depths:
					out = tdfolder + '/Criterion=' + criterion + '_Splitter=' + splitter + '_MaxFeat=' + max_feature + '_MaxDepth=' + max_depth + '.txt'
					comm = 'nohup python DecisionTree.py ' + criterion + ' ' + splitter + ' ' + max_feature + ' ' + max_depth + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
					print(comm)
					os.system(comm)
