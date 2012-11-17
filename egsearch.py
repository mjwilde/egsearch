#! /usr/bin/env python
'''
Sam Volchenboum

'''
#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)

import time
import os
import errno
import sys
from   sklearn.svm import SVC
from   sklearn.preprocessing import scale
import numpy as np
from   itertools import combinations, islice
from   scipy.stats import ttest_ind
from   math import factorial, ceil

def write_file(output_file, filename, add_cr = True):
	'''Writes output_file to filename'''
	newfile = open(filename, "w")
	for a in output_file:
		if (add_cr == True):
			newfile.write(a+"\n")
		else:
			newfile.write(a)
	return

def readfile(name_of_file, cr = 1):
	print "Loading\t\t\t"+ name_of_file
	file_data = open(name_of_file)
	file_contents = file_data.readlines()
	output = []
	for i,line in enumerate(file_contents):
		if (i <> len(file_contents)-1): # no CR on last line, apparently
			output.append(line[:(-1* cr)]) # strip carriage returns
		else:
			output.append(line)
	return output

def load_data(filename):
	D = readfile(filename,".")
	D = D[0].split('\r')
	D = [a.split(',') for a in D]
	D = [D[0]] + [D[1]] + [t[0:5] + [float(a) for a in t[5:]] for t in D[2:]]
	return D
	
def ranktest(D):
	# set up comparison test for the two groups
	D = D[2:] # get rid of header and phenotype data rows
	for line in D: # row one is sample names, row two is classes
		S1 =  [float(line[x+5]) for x,a in enumerate(training_labels) if a == 0]
		S2 =  [float(line[x+5]) for x,a in enumerate(training_labels) if a == 1]
		T = ttest_ind(S1,S2)
		line.append(float(T[0]))
	D.sort(lambda a,b:cmp(abs(b[-1]),abs(a[-1]))) # sort descending order by t-test. The t-test value is at the end of the row
	D = [[l[0]] + l[1] for l in enumerate(D)] # adds in original sort order for each line so we can see quickly later how differentially expressed something was
	
	if rank <> True: # this means that rank is a number (and not False) and that we should only keep a certain number of rows
		D = D[:rank]
	return D

def test_combos(D):
	
	d = ',' # divider for output file	
	print "Features\t\t",len(D)

	Y = np.array(training_labels)
	C = 1.0
	for combo in combos_to_test:

		#groups = combinations(D[2:],combo)
		groups = combinations(D,combo)
		#
		# number of groups will be
		#
		#              n!
		#          ----------
		#          (n-r)! r!
		#
		# n = number of features
		# r = number chosen
		# assumes order not important and no repetition allowed
		# http://www.mathsisfun.com/combinatorics/combinations-permutations-calculator.html
		#
		#
		total = factorial((len(D))) / (factorial(len(D) - combo)  * factorial(combo) ) 
		print "Total combinations\t",total
		print "Taking at a time\t",combo

		numSlices   = int(sys.argv[1])
		sliceNumber = int(sys.argv[2])
		outFileName = sys.argv[3]

                iterPerGroup = int(ceil(float(total)/float(numSlices))) 
		firstIter = sliceNumber * iterPerGroup

		print "Number of slices\t", numSlices
		print "Slice number\t\t",sliceNumber
		print "Iterations per group\t", iterPerGroup
		print "First iteration\t\t", firstIter
		print "Last iteration\t\t", firstIter+iterPerGroup
		print "outFileName\t\t", outFileName
		print
		
		slices = [ islice(groups,firstIter,firstIter+iterPerGroup) ]

		for slice_number,S in enumerate(slices): # FIXME: eiminate this loop
			output = []	
			counter = 0
			for group in S:
				if counter%10000 == 0: print "Doing combination\t", counter
				counter += 1
				sym = [str(a[0]+1) +'*'+ a[2]+'^'+a[4] for a in group]
				if rank:
					lines = [[float(a) for a in b[6:-1]] for b in group] # the -1 is to remove the t-test parameter at the end
				else:
					lines = [[float(a) for a in b[6:]] for b in group] 
				training_data = zip(*lines)
				X = np.array(training_data)
				X = scale(X)
				n_features = X.shape[1]
				#name =  'Linear SVC'
				clf = SVC(kernel='linear', C=C, probability=True)
				clf.fit(X, Y)
				y_pred = clf.predict(X)
				classif_rate = np.mean(y_pred.ravel() == Y.ravel()) * 100
				if classif_rate > threshold:
					output.append([sym,classif_rate])
					if screen_output:
						print sym, classif_rate
			output = [','.join([a.split('*')[0] + d + a.split('^')[0].split('*')[1] +d + a.split('^')[1] for a in line[0]])  + (d * ((max(combos_to_test) - len(line[0])) * 2))+ d + str(line[1]) for line in output]
			write_file(output,outFileName)
		print "Final combination\t", counter

'''User modifiable variables'''	

# to run a true exhaustive search: save_data = False, rank = False, threshold = 98, combos_to_test = [1,2]
# this will limit the combos to one and two features and save anything with a classification > 98%

#save_data = False # If true, will save the raw data in the output file	

rank = True # can either be False / True or a number, in which case it is the number of top and bottom features to keep
threshold = 95 # only save data if classification rate greater than this number.
screen_output = False
combos_to_test = [2] # numbers of features to test
number_of_slices = 10
results_filename = '/home/wilde/Projects/Sam/esearch'+'/'+'williamson_genes_normalized_all.csv' # FIXME: ship via swift

'''Should not need to change anything below this line'''

#working_folder = "./"
#timestamp = str(int(time.time()))
#os.mkdir(working_folder + timestamp) # create output directory

#data = load_data(working_folder + results_filename)
data = load_data(results_filename)

training_labels = [0 if a == "Neg" else 1 for a in data[1][5:]] # this only allows for two classes. Need to generalize
if rank:
	data = ranktest(data)
#data = data[0:400]
output = test_combos(data)
# joinslices()
