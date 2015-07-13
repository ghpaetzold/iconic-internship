import os

#Set language pair:
lang_pair = 'es-en'

#Parameters:
Cs = ['1.0', '10.0']
kernels = ['rbf', 'sigmoid', 'linear']
degrees = ['2']
gammas = ['0.0', '1.0', '10.0']
coef0s = ['0.0', '1.0']
ks = ['40', 'all']

#Files:
trainDataset = 'dataset1'
testDatasets = ['dataset1', 'dataset2']
testDatasets = ['dataset1']
trainX = '../../corpora/'+lang_pair+'/features/'+trainDataset+'_train.features_noppl'
trainY = '../../corpora/'+lang_pair+'/datasets/'+trainDataset+'_train.classes'

#Folder name:
folder = 'svm'
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

	if 'rbf' in kernels:
		for C in Cs:
			for gamma in gammas:
				for k in ks:
					out = tdfolder + '/svc_rbf_C=' + C + '_Gamma=' + gamma + '_K=' + k + '.txt'
					model = modelfolder + '/svc_rbf_C=' + C + '_Gamma=' + gamma + '_K=' + k + '.bin'
					comm = 'nohup python SVM.py ' + C + ' rbf 1 ' + gamma + ' 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' + model + ' &'
					print(comm)
					os.system(comm)
	
	if 'poly' in kernels:
	        for C in Cs:
	                for gamma in gammas:
				for degree in degrees:
					for coef0 in coef0s:
						for k in ks:
				                        out = tdfolder + '/svc_poly_C=' + C + '_Gamma=' + gamma + '_Degree=' + degree + '_Coef0=' + coef0
							out += '_K=' + k +  '.txt'
							model = modelfolder + '/svc_poly_C=' + C + '_Gamma=' + gamma + '_Degree=' + degree + '_Coef0=' + coef0
							model += '_K=' + k +  '.bin'
				                        comm = 'nohup python SVM.py ' + C + ' poly ' + degree + ' ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' + model + ' &'
				                        print(comm)
				                        os.system(comm)
	
	if 'sigmoid' in kernels:
	        for C in Cs:
	                for gamma in gammas:
	                        for degree in degrees:
	                                for coef0 in coef0s:
						for k in ks:
		                                        out = tdfolder + '/svc_sigmoid_C=' + C + '_Gamma=' + gamma + '_Coef0=' + coef0 + '_K=' + k + '.txt'
							model = modelfolder + '/svc_sigmoid_C=' + C + '_Gamma=' + gamma + '_Coef0=' + coef0 + '_K=' + k + '.bin'
		                                        comm = 'nohup python SVM.py ' + C + ' sigmoid 1 ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' + model + ' &'
		                                        print(comm)
		                                        os.system(comm)
	if 'linear' in kernels:
	        for C in Cs:
			for k in ks:
				out = tdfolder + '/svc_linear_C=' + C + '_K=' + k + '.txt'
				model = modelfolder + '/svc_linear_C=' + C + '_K=' + k + '.bin'
				comm = 'nohup python SVM.py ' + C + ' linear 1 0.0 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + k + ' ' + out + ' ' +  model + ' &'
				print(comm)
				os.system(comm) 
