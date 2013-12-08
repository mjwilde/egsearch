
'''



'''


#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)
import time
import os
from sklearn.svm import SVC
from sklearn.preprocessing import scale
import numpy as np
from itertools import combinations
from scipy.stats import ttest_ind
from math import factorial


def write_file(output_file, filename, directory='.', add_cr = True):
	'''Writes output_file to filename'''
	newfile = open(directory+"/"+filename+".csv", "w")
	for a in output_file:
		if (add_cr == True):
			newfile.write(a+"\n")
		else:
			newfile.write(a)
	return

def readfile(name_of_file, directory=".", cr = 1):
	print "Loading "+name_of_file+"..."
	file_data = open(directory+"/"+name_of_file)
	file_contents = file_data.readlines()
	output = []
	for i,line in enumerate(file_contents):
		if (i <> len(file_contents)-1): # no CR on last line, apparently
			output.append(line[:(-1* cr)]) # strip carriage returns
		else:
			output.append(line)
	return output

def load_data(filename):
	D = readfile(results_filename,".")
	D = D[0].split('\r')
	D = [a.split(',') for a in D]
	D = [D[0]] + [D[1]] + [t[0:5] + [float(a) for a in t[5:]] for t in D[2:]]
	return D
	
def ranktest(D):
	# set up comparison test for the two groups
	for line in D[2:]: # row one is sample names, row two is classes
		S1 =  [float(line[x+5]) for x,a in enumerate(training_labels) if a == 0]
		S2 =  [float(line[x+5]) for x,a in enumerate(training_labels) if a == 1]
		T = ttest_ind(S1,S2)
		line.append(T[0])
	D.sort(lambda a,b:cmp(b[-1],a[-1]))
	D = D[:rank] + D[-1 * rank:]
	return D

def test_combos(D):
	# going to test each line in D against every other
	output = []
	print "There are",len(D),"features."
	print
	for combo in combos_to_test:
		print
		print "Taking",combo,"at a time."
		groups = combinations(D[2:],combo)
		#
		# number of groups will be
		#
		#              n!
		#          ----------
		#          (n-r)! r!
		#
		# n = number of features
		# r = number chosen
		# assumes orer not important and no repetition allowed
		# http://www.mathsisfun.com/combinatorics/combinations-permutations-calculator.html
		#
		#
		total = factorial((len(D))) / (factorial(len(D) - combo)  * factorial(combo) ) 
		print "There are",total,"combinations."
		counter = 0
		for group in groups:
			if counter%1000 == 0: print counter
			counter += 1
			sym = [a[1]+'^'+a[3] for a in group]
			if rank:
				lines = [[float(a) for a in b[5:-1]] for b in group] # the -1 is to remove the t-test parameter at the end
			else:
				lines = [[float(a) for a in b[5:]] for b in group] # the -1 is to remove the t-test parameter at the end
			training_data = zip(*lines)
			X = np.array(training_data)
			X = scale(X)
			Y = np.array(training_labels)
			n_features = X.shape[1]
			C = 1.0
			#name =  'Linear SVC'
			clf = SVC(kernel='linear', C=C, probability=True)
			clf.fit(X, Y)
			y_pred = clf.predict(X)
			classif_rate = np.mean(y_pred.ravel() == Y.ravel()) * 100
			if classif_rate > threshold and save_data:
				points = [[a[n] for a in X] for n in range(combo)] # the raw data to save later
				output.append([sym,classif_rate,points])
			elif classif_rate > threshold:
				output.append([sym,classif_rate])

	output.sort(lambda x,y:cmp(y[1],x[1]))
	return output

def write_output(output):
	d = ','
	newout = [','.join(['probe,symbol'] * max(combos_to_test)) + d + 'Classification'] 
	for line in output:
		if save_data:
			newline = ','.join([a.split('^')[0] +d + a.split('^')[1] for a in line[0]])  + (d * ((max(combos_to_test) - len(line[0])) * 2))+ d + str(line[1])  + d + ','.join([','.join([str(c) for c in b]) + ',' for b in line[2]])
		else:
			newline = ','.join([a.split('^')[0] +d + a.split('^')[1] for a in line[0]])  + (d * ((max(combos_to_test) - len(line[0])) * 2))+ d + str(line[1]) 
		newout.append(newline)
	write_file(newout, "output_data", directory=timestamp, add_cr = True)
	return

'''User modifiable variables'''	
# to run a true exhaustive search: save_data = False, rank = False, threshold = 98, combos_to_test = [1,2]
# this will limit the combos to one and two features and save anything with a classification > 98%
save_data = False # If true, will save the raw data in the output file	
rank = False # can either be False or a number, in which case it is the number of top and bottom features to keep
threshold = 98 # only save data if classification rate greater than this number.
combos_to_test = [1,2] # numbers of features to test
results_filename = 'williamson_genes_normalized_all.csv'
'''Should not need to change anything below this line'''

working_folder = "./"
timestamp = str(int(time.time()))
os.mkdir(working_folder + timestamp) # create output directory
data = load_data(working_folder + results_filename)
training_labels = [0 if a == "Neg" else 1 for a in data[1][5:]] # this only allows for two classes. Need to generalize
if rank:
	data = ranktest(data)
#t0 = time.time()
output = test_combos(data)
#print time.time() - t0, "seconds"
write_output(output)
