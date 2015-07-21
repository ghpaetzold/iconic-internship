import os, copy

#Set language pair:
lang_pair = 'es-en'

#Files:
trainDataset = 'dataset3'
testDatasets = ['dataset1', 'dataset2']
#testDatasets = ['dataset1']

#Folder name:
folder = 'svmjava'
os.system('mkdir ../../classes/'+lang_pair)
os.system('mkdir ../../classes/'+lang_pair+'/'+folder)

#Get models:
os.system('mkdir /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair)
modelfile = '../../models/'+lang_pair+'/'+folder+'/'+trainDataset+'/Folds=0_Kernel=rbfnonorm.bin'

#Get models:
for td in testDatasets:
	os.system('mkdir ../../classes/'+lang_pair+'/'+folder+'/'+td)

	tdfolder = '../../classes/'+lang_pair+'/'+folder+'/'+td
	outfile = tdfolder + '/'+trainDataset+'_Folds=0_Kernel=rbfnonorm.bin'
	featuresFile = '../../corpora/'+lang_pair+'/features/'+td+'_test.features_noppl'

	comm = 'java -cp /export/data/ghpaetzold/iconicinternship/java/IconicQualityEstimator/IconicQualityEstimator.jar main.EstimateQuality '
	comm += '-temp /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair+'/'+trainDataset+'/ '
	comm += '-model ' + modelfile + ' '
	comm += '-featurevalues ' + featuresFile + ' '
	comm += '-output ' + outfile + ' '
	print(str(comm))	
	os.system(comm)
