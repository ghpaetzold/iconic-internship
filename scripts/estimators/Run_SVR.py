import os

#Parameters:
Cs = ['0.1', '1.0', '10.0']
epsilons = ['0.1', '0.01']
kernels = ['rbf', 'poly', 'sigmoid', 'linear']
kernels = ['sigmoid', 'linear']
degrees = ['2']
gammas = ['0.0', '1.0', '10.0']
coef0s = ['0.0', '1.0']

#Files:
trainX = '../../corpora/features.train.txt'
trainY = '../../corpora/scores.txt'
testX = '../../corpora/features.train.txt'
testY = '../../corpora/scores.txt'

#Folder name:
folder = 'svm_svr'
os.system('mkdir ../../scores/' + folder)

#Run all configurations in parallel:
if 'rbf' in kernels:
	for C in Cs:
		for epsilon in epsilons:
			for gamma in gammas:
				out = '../../scores/' + folder + '/rbf_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '.txt'
				comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' rbf 1 ' + gamma + ' 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
				print(comm)
				os.system(comm)

if 'poly' in kernels:
        for C in Cs:
		for epsilon in epsilons:
	                for gamma in gammas:
				for degree in degrees:
					for coef0 in coef0s:
			                        out = '../../scores/' + folder + '/poly_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '_Degree=' + degree + '_Coef0=' + coef0 + '.txt'
			                        comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' poly ' + degree + ' ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
			                        print(comm)
			                        os.system(comm)

if 'sigmoid' in kernels:
        for C in Cs:
		for epsilon in epsilons:
	                for gamma in gammas:
	                        for degree in degrees:
	                                for coef0 in coef0s:
	                                        out = '../../scores/' + folder + '/sigmoid_C=' + C + '_Epsilon=' + epsilon + '_Gamma=' + gamma + '_Coef0=' + coef0 + '.txt'
	                                        comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' sigmoid 1 ' + gamma + ' ' + coef0 + ' ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
	                                        print(comm)
	                                        os.system(comm)
if 'linear' in kernels:
        for C in Cs:
		for epsilon in epsilons:
			out = '../../scores/' + folder + '/linear_C=' + C + '_Epsilon=' + epsilon + '.txt'
			comm = 'nohup python SVR.py ' + C + ' ' + epsilon + ' linear 1 0.0 0.0 ' + trainX + ' ' + trainY + ' ' + testX + ' ' + testY + ' ' + out + ' &'
			print(comm)
			os.system(comm)
