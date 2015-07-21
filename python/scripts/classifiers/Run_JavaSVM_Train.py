import os, copy

#Set language pair:
lang_pair = 'en-es'

#Parameters:
folds = ['5', '10']
folds = ['0']
kernels = ['rbf', 'sigmoid', 'linear']
kernels = ['rbf']

#Files:
trainDataset = 'dataset3'

#Folder name:
folder = 'svmjava'
os.system('mkdir ../../models/'+lang_pair)
os.system('mkdir ../../models/'+lang_pair+'/'+folder)
os.system('mkdir ../../models/'+lang_pair+'/'+folder+'/'+trainDataset)

#Get models:
os.system('mkdir /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair)
os.system('mkdir /export/data/ghpaetzold/iconicinternship/temp/'+lang_pair+'/'+trainDataset)
modelfolder = '../../models/'+lang_pair+'/'+folder+'/'+trainDataset	

sourceFile = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.zh'
targetFile = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.en'
scoresFile = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'
featuresFile = '../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features_noppl'

comm = 'java -cp /export/data/ghpaetzold/iconicinternship/java/IconicQualityEstimator/IconicQualityEstimator.jar main.GetQualityModel '
comm += '-featurevalues ' + featuresFile + ' '
comm += '-scores ' + scoresFile + ' '

for fold in folds:
	for kernel in kernels:
		temp_folder = '/export/data/ghpaetzold/iconicinternship/temp/'+lang_pair+'/'+trainDataset+'/'+str(fold)+str(kernel)
		os.system('mkdir '+temp_folder)

		model_file = modelfolder + '/Folds=' + str(fold) + '_Kernel=' + str(kernel) + 'nonorm.bin'

		fcomm = copy.copy(comm)
		fcomm += '-folds ' + str(fold) + ' '
		fcomm += '-kernel ' + str(kernel) + ' '
		fcomm += '-temp ' + str(temp_folder) + ' '
		fcomm += '-model ' + model_file + ' '
		fcomm += '-C 10.0 '
		fcomm += '-gamma 10.0 '
		fcomm += '-epsilon 0.001 > ' + lang_pair+str(fold)+str(kernel)+'.txt &'
		print(str(fcomm))	
		os.system(fcomm)
