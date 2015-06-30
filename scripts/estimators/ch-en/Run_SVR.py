import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
Cs = ['0.1', '1.0', '10.0']
epsilons = ['0.1', '0.01']
kernels = ['rbf', 'sigmoid', 'linear']
degrees = ['2']
gammas = ['0.0', '1.0', '10.0']
coef0s = ['0.0', '1.0']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.scores'

#Folder name:
folder = 'svm'
os.system('mkdir ../../../scores/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
        os.system('mkdir ../../../scores/'+lang_pair+'/'+folder+'/'+td)

        tdfolder = '../../../scores/'+lang_pair+'/'+folder+'/'+td

        testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
        testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.scores'

	#Run all configurations in parallel:
	if 'rbf' in kernels:
		for C in Cs:
			for epsilon in epsilons:
				for gamma in gammas:
					out = tdfolder + '/svr_rbf_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '.txt'
					comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' rbf 1 ' + gamma + ' 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
					print(comm)
					os.system(comm)
	
	if 'poly' in kernels:
	        for C in Cs:
			for epsilon in epsilons:
		                for gamma in gammas:
					for degree in degrees:
						for coef0 in coef0s:
				                        out = tdfolder + '/svr_poly_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '_Degree=' + degree + '_Coef0=' + coef0 + '.txt'
				                        comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' poly ' + degree + ' ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
				                        print(comm)
				                        os.system(comm)
	
	if 'sigmoid' in kernels:
	        for C in Cs:
			for epsilon in epsilons:
		                for gamma in gammas:
		                        for degree in degrees:
		                                for coef0 in coef0s:
		                                        out = tdfolder + '/svr_sigmoid_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '_Coef0=' + coef0 + '.txt'
		                                        comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' sigmoid 1 ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
		                                        print(comm)
		                                        os.system(comm)
	if 'linear' in kernels:
	        for C in Cs:
			for epsilon in epsilons:
				out = tdfolder + '/svr_linear_C=' + C + '_Epsilon=' + epsilon + '.txt'
				comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' linear 1 0.0 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
				print(comm)
				os.system(comm)
