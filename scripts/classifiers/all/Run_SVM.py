import os

#Set language pair:
lang_pair = 'ch-en'

#Parameters:
Cs = ['1.0', '10.0']
kernels = ['rbf', 'sigmoid', 'linear']
kernels = ['rbf', 'sigmoid']
degrees = ['2']
gammas = ['0.0', '1.0', '10.0']
gammas = ['1.0', '10.0']
coef0s = ['0.0', '1.0']
ks = ['50', '60', '65']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
trainX = '../../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features'
trainY = '../../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'svm'
os.system('mkdir ../../../classes/'+lang_pair+'/'+folder)

#Get models:
for td in testDatasets:
	os.system('mkdir ../../../classes/'+lang_pair+'/'+folder+'/'+td)
	
	tdfolder = '../../../classes/'+lang_pair+'/'+folder+'/'+td

	testX = '../../../corpora/'+lang_pair+'/features/'+td+'_test.features'
	testY = '../../../corpora/'+lang_pair+'/datasets/'+td+'_test.classes'

	if 'rbf' in kernels:
		for C in Cs:
			for gamma in gammas:
				for k in ks:
					out = tdfolder + '/svc_rbf_C=' + C + '_Gamma=' + gamma + '_K=' + k + '.txt'
					comm = 'nohup python SVM.py ' + C + ' rbf 1 ' + gamma + ' 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
					print(comm)
					os.system(comm)
	
	if 'poly' in kernels:
	        for C in Cs:
	                for gamma in gammas:
				for degree in degrees:
					for coef0 in coef0s:
						for k in ks:
				                        out = tdfolder + '/svc_poly_C=' + C + '_Gamma=' + gamma + '_Degree=' + degree + '_Coef0=' + coef0 +'_K=' + k +  '.txt'
				                        comm = 'nohup python SVM.py ' + C + ' poly ' + degree + ' ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
				                        print(comm)
				                        os.system(comm)
	
	if 'sigmoid' in kernels:
	        for C in Cs:
	                for gamma in gammas:
	                        for degree in degrees:
	                                for coef0 in coef0s:
						for k in ks:
		                                        out = tdfolder + '/svc_sigmoid_C=' + C + '_Gamma=' + gamma + '_Coef0=' + coef0 + '_K=' + k + '.txt'
		                                        comm = 'nohup python SVM.py ' + C + ' sigmoid 1 ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
		                                        print(comm)
		                                        os.system(comm)
	if 'linear' in kernels:
	        for C in Cs:
			for k in ks:
				out = tdfolder + '/svc_linear_C=' + C + '_K=' + k + '.txt'
				comm = 'nohup python SVM.py ' + C + ' linear 1 0.0 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' &'
				print(comm)
				os.system(comm) 
