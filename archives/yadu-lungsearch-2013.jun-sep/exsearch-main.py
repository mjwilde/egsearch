#! /usr/bin/env python
'''
Sam Volchenboum

Loads in CSV with data in rows. 
First row are headers.
data file is <results_filename>
Rows zero to <data_row_start> are phenotype information.
<rank> designates whether or not to perform a T-test on the data and rank the features.
If <rank> is not False, then it should be a number. This is the number of top/bottom rows to take from the sorted list (i.e. most positive and most negative)
If <rank> is False, then all data will be used, unranked.  This will take a long, long time.
<combos_to_test> are the numbers of features to group together.
For instance, if the features are [a,b,c,d,e] and <combos_to_test> is [1,2] then the groups will be [a,b,c,d,e,ab,ac,ad,ae,bc,bd,be,cd,ce,de] and so forth.
If <print_to_screen> is True, then output will include the classifiers that are highest ranked as well as the raw data for each to be copied and pasted into a graphing program
If <save_data> = True, will write all points for classification rate better than <save_rank>
If <save_data> = False, will write nothing for classification rate less than <save_rank>
<library_name> = annotation file from Affymetrix

Usage notes: python exsearch.py 100 10 aout -Scott 05/30/2013 skrieder@iit.edu
'''
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import time
#import pylab as pl
import numpy as np
import os

#from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
#from sklearn import datasets
from sklearn.preprocessing import scale
#from itertools import izip
from itertools import combinations, islice
from scipy.stats import tmean, ttest_ind
#from numpy import std
#from random import randint
from math import factorial, ceil
from operator import itemgetter, attrgetter
import sys

# DD = [[1,22000],[4,22000],[3,22000],[2,22000]]
# #DD = [[5,20]]
# for D in DD:
# 	Y = D[0]
# 	X = D[1] * 2
# 	total = factorial((X)) / (factorial(X - Y)  * factorial(Y) ) 
# 	print X,Y,total
# 	
# exit()

def write_file(output_file, filename, directory='.', add_cr = True):
	'''Writes output_file to filename'''
	newfile = open(filename, "w")
	for a in output_file:
		if (add_cr == True):
			newfile.write(a+"\n")
		else:
			newfile.write(a)
	return

def readfile(name_of_file, directory=".", cr = 1):
	print "Loading "+name_of_file+"..."
	# 
	# print "NAME",name_of_file, type(name_of_file)
	# print "DIR",directory, type(directory)
	# 
	file_data = open(directory+"/"+name_of_file)
	file_contents = file_data.readlines()
	output = []
	for i,line in enumerate(file_contents):
		if (i <> len(file_contents)-1): # no CR on last line, apparently
			output.append(line[:(-1* cr)]) # strip carriage returns
		else:
			output.append(line)
	return output

def load_data(filename,f,r): #r = starting row for the data
	D = readfile(results_filename,f)
	D = [a.replace('\r','').split(',') for a in D]
	D = D[0:r] + [[a[0]] + [float(b) for b in a[1:]] for a in D[r:]]
	return D
	
def ranktest(D,training_labels,r):
	# set up comparison test for the two groups
	# assumes two groups are [0,1]
	for line in D[r:]: # row one is sample names, row two is classes
		S1 =  [float(line[x+1]) for x,a in enumerate(training_labels) if a == 0]
		S2 =  [float(line[x+1]) for x,a in enumerate(training_labels) if a == 1]
		T = ttest_ind(S1,S2)
		line.append(T[0])
		
	D[r:] = sorted(D[r:], key=itemgetter(-1), reverse=True) # sort by value of T-test positive to negative
	D = D[:r] + D[r:r+rank] + D[-1 * rank:] # rank is a number. keep the top and bottom "rank" number of samples
	D[r:] = sorted(D[r:], key = lambda x: abs(x[-1]), reverse=True) # sorts by absolute value of T-test
	D =  D[:r]  + [a[1] + [a[0]+1] for a in enumerate(D[r:])] # numbers each one at end
	D[r:] = sorted(D[r:], key=itemgetter(-2), reverse=True) # sorts again by relative value of t-test
	return D

def test_combos(d,training_labels,r):
	# going to test each line in D against every other
	D = d[r:]
	max_class = 50.0 # starting baseline for classification
	output = []
	print "There are",len(D),"features."
	if print_to_screen:
		for line in d[0][1:]:
			print line
		print
		print
		for line in training_labels:
			print line
		print
		print
	
	FOX = ['202580_x_at', 8.92, 7.59, 6.72, 6.18, 7.11, 8.4, 7.87, 6.87, 6.34, 6.17, 6.52, 6.84, 7.01, 7.54, 6.4, 6.88, 7.14, 7.04, 6.68, 6.95, 6.9, 6.76, 6.35, 7.65, 6.55, 8.21, 6.68, 7.25, 7.07, 6.65, 8.15, 6.62, 9.21, 6.8, 7.68, 6.9, 6.66, 6.32, 7.54, 6.17, 6.5, 8.24, 7.56, 7.18, 8.24, 6.67, 6.83, 7.69, 7.93, 7.29, 6.44, 6.44, 7.15, 7.51, 6.08, 6.41, 5.69, 7.14, 7.54, 7.55, 6.96, 6.43, 6.15, 8.68, 7.36, 8.88, 7.04, 6.21, 2.2983938427111705, 794]	
	
	for combo in combos_to_test:
		print
		print "Taking",combo,"at a time."
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
		# assumes orer not important and no repetition allowed
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
			for group in groups:
				#group = [a for a in group] + [FOX] # for adding FOXM1
	
				# for line in group:
				# 	print line
				# 	print len(line)
				# 	print
				# exit()
	
				if counter%10000 == 0: print counter
				counter += 1
			
				if rank:
					sym = [a[0]+" , "+lib[a[0]][7]+" , "+lib[a[0]][8]+" , "+str(a[-1]) for a in group]
					lines = [[float(a) for a in b[1:-2]] for b in group] # remove the t-test and rank
				
					# print sym
					# for line in lines:
					# 	print line
					# 	print len(line)
					# 	print
					# exit()
					# 
				
				else:
					sym = [a[0]+" , "+lib[a[0]][7]+" , "+lib[a[0]][8] for a in group]
					lines = [[float(a) for a in b[1:]] for b in group] 				
				training_data = zip(*lines)
				X = np.array(training_data)
				X = scale(X)
				Y = np.array(training_labels)

				n_features = X.shape[1]
				C = 1.0
				name =  'Linear SVC'
				clf = SVC(kernel='linear', C=C, probability=True)
				clf.fit(X, Y)
				y_pred = clf.predict(X)
				classif_rate = np.mean(y_pred.ravel() == Y.ravel()) * 100
			
				# if classif_rate > 80 and '202580_x_at' in [a.split(',')[0].replace(' ','') for a in sym]:
				# 	print classif_rate, sym
			
				if classif_rate > 89:
					print classif_rate, sym
			
				# print sym
				# if 'ARNTL2' in sym:	
				# 	print sym, classif_rate
			
				if print_to_screen and classif_rate > max_class: # keep track of the best combo so far...	
					points = [[a[n] for a in X] for n in range(combo)]
					print sym,classif_rate
					if print_to_screen == "points":
						for P in points:
							for p in P:
								print p
							print
							print "-------------------------------------------------"
					max_class = classif_rate
				if classif_rate >= save_rank: # save all the data. If you want all data for everything, make save_data = True, and save_rank = 0
					points = [[a[n] for a in X] for n in range(combo)] # the raw data to save later
					#print points
					#exit()
					output.append([sym,classif_rate,points])
				elif classif_rate < save_rank and save_data: # 
					output.append([sym,classif_rate]) # if save_data = False or 0, only save the features and rate - but not the data
				elif save_data == False:
					continue
			output.sort(lambda x,y:cmp(y[1],x[1]))
			#print "SUB",subname
			#print "TYPE",type(working_folder),type(timestampe),type(subname)
			# newfilename = working_folder + "/" + timestamp + "/" + outFileName
			newfilename = outFileName
			# print "NNAME",newfilename
			# exit()
			write_output(output,newfilename)
	return output

def write_output(output, filename):
	#combos_to_test = [3]
	d = ','
	
	
	if rank:
		leader = ['Probe','Name','Symbol','Rank']
	else:
		leader = ['Probe','Name','Symbol']
	
	newout = [data_files, metrics, description] + [','.join(leader * max(combos_to_test)) + d + 'Classification' + d + (d.join(samples) + ", ,") * max(combos_to_test)] + [ d * (len(leader) * max(combos_to_test)) + "," + (d.join([str(a) for a in training_labels]) + ", ,") * max(combos_to_test)]
	
	for line in output:
		#print ','.join([','.join([str(c) for c in b]) + ',' for b in line[2]])
		#exit()
		if len(line) == 3:
			newline = ','.join([a for a in line[0]])  + d * len(leader) * (max(combos_to_test) - len(line[0])) + d + str(line[1]) + d + ','.join([','.join([str(c) for c in b]) + ',' for b in line[2]])
		else:
			newline = ','.join([a for a in line[0]])  + d * len(leader) * (max(combos_to_test) - len(line[0])) + d + str(line[1]) 
		newout.append(newline)

	write_file(newout, filename, add_cr = True)
	return

def get_library(library,r):
	# creates dictionary of probes and symbols
	'''
	0 Probe Set ID
	1 Transcript ID(Array Design)
	2 Target Description
	3 Representative Public ID
	4 Archival UniGene Cluster
	5 UniGene ID
	6 Alignments
	7 Gene Title
	8 Gene Symbol
	9 Chromosomal Location
	10 Unigene Cluster Type
	11 Ensembl
	12 Entrez Gene
	13 SwissProt
	14 EC
	15 OMIM
	16 RefSeq Protein ID
	17 RefSeq Transcript ID
	18 Gene Ontology Biological Process
	19 Gene Ontology Cellular Component
	20 Gene Ontology Molecular Function
	21 Pathway
	22 InterPro
	23 Annotation Transcript Cluster
	24 Transcript Assignments
	25 Annotation Notes
	'''

	lib = readfile(library, r)
	lib = [line.split(',') for line in lib]
	lib_d = {}
	for line in lib:
		lib_d[line[0]] = line
	return lib_d


print_to_screen = False	# True, False, "points"
save_data = False # save all data, including data points, for classif_rate greater than save_rank below. If false, will record all data for above save rank and nothing for less than save rank.
save_rank = 85.0 # cut-off for saving data. If 100, and save_data = True, will save only classification rate for everything. If 0.0 and True above, will write full data for every line
# for example, save_data = True, save_rank = 80.0, will save all data for above 80% and only classitification rate for less than 80%
# for example, save_data = False, save_rank = 80, will save all data for above 80% and nothing for less than 80%
# if save_data = True, and save_rank = 100.0, will save rate only for everything. If rank = 0, will save all points for everything
rank = 10 # can either be false or a number, in which case it is the number of top and bottom features to keep after t-test. False means no t-test, use all features
combos_to_test = [2] # numbers of features to test. e,g, 1,2 means test all single gene and then all two gene combos
data_row_start = 14 # data starts at this row
#feature,feature_index,values = "Death",4,[0,1]


library_name = 'HG-U133A_2.na33.annot.csv'
working_folder = "./"
lib = get_library(library_name,working_folder) # dictionary of probes and symbols
timestamp = str(int(time.time()))
if not os.path.isdir(working_folder + "/" + timestamp):
	os.mkdir(working_folder + "/" + timestamp) # create output directory
#results_filename = 'Lung_Cancer_Sample_Data.csv'
results_filename = 'Consortium_expr_full_pheno_no_affx.csv'
data = load_data(results_filename,working_folder,data_row_start)
'''
0 UniqueID
1 histology
2 had_adjuvant_chemo (TRUE/FALSE)
3 recurrence
4 TimetoRecurrence
5 death
6 overall_survival_months
7 age
8 gender
9 stage.title
10 dataset.id
11 had_adjuvant_RT
12 FirstProgressionOrRelapse
13 TimetoFirstProgression
'''


# Here is the data selection section
# clunky but works
# choose elements from list above
# metrics hard coded
data_files = "Data source = " + library_name + ", library = " + library_name
metrics = "Save rank = " + str(save_rank) + ", save_data = " + str(save_data) + ", rank = " + str(rank) + ", combos_to_test = " + str(combos_to_test) 
L = 24.0
H = 48.0
description = "Adjuvant chemotherapy, <" + str(L) + " months vs. > " + str(H) + " months"
data_using = [[line[0]] +  [a[1] for a in enumerate(line[1:]) if  (data[2][a[0]+1] == 'FALSE' and data[6][a[0]+1] <> "NA") and (float(data[6][a[0]+1]) < L or float(data[6][a[0]+1]) > H)] for line in data]
training_labels = [0 if float(a) < L  else 1 for a in data_using[6][1:]] 
samples = [a for a in data_using[0][1:]]
#print samples
categories = [len([a for a in training_labels if a == 0]),len([a for a in training_labels if a == 1])]
description = description + "_" + str(categories[0]) + "_" + str(categories[1]) + "_" + "Top " + str(rank)

if print_to_screen:
	print description

if rank:
	data = ranktest(data_using,training_labels,data_row_start)
else:
	data = data_using
	
# combos_to_test = [1,2,3,4,5]
# D = data
# for combo in combos_to_test:
# 	total = factorial((len(D))) / (factorial(len(D) - combo)  * factorial(combo) ) 
# 	print combo,total
# exit()

# <24 vs >48 = 794
# <12 vs >24 = 10591
# <12 vs >48 = 6998
# <12 vs >60 = 8242
# <6 vs >60 2108
# <24 >24 1777
# 24 36 1205
# 12 36 8629
#24 30 1900


# test = '202580_x_at'
# for line in data:
# 	if line[0] == test:
# 		print line
# 		print
# exit()


# for i,line in enumerate(data):
# 	print i,line
# exit()
output = test_combos(data, training_labels,data_row_start)
#write_output(output)
	
#exit()


