import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
Cs = ['1.0', '10.0']
kernels = ['rbf', 'sigmoid', 'linear']
gammas = ['0.0', '1.0', '10.0']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']

#Folder name:
folder = 'svmjava'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
	os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)
	os.system('mkdir /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair)
	os.system('mkdir /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair+'/'+td)
	
	tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

	testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features_noppl'
	testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	comm = 'nohup java -cp /export/data/ghpaetzold/iconicinternship/java/IconicQualityEstimator/IconicQualityEstimator.jar main.GetQualityModel '
	comm += '-temp /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair+'/'+td+' '
	comm += '-features /export/data/ghpaetzold/iconicinternship/corpora/features_noppl.xml '
	comm += '-giza /export/data/ghpaetzold/iconicinternship/corpora/ch-en/resources/ICONICGIZA.actual.ti.final '
	comm += '-ngramsrc /export/data/ghpaetzold/iconicinternship/corpora/ch-en/resources/ngram_counts.clean.zh.clean '
	comm += '-corpussrc /export/data/ghpaetzold/iconicinternship/corpora/ch-en/large/sample/train.sample.zh'
	
