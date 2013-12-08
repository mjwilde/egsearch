#! /usr/bin/env python

#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)

import os
import sys
import glob

def write_file(output_file, filename, directory='.', add_cr = True):
	'''Writes output_file to filename'''
	newfile = open(directory+"/"+filename, "w")
	for a in output_file:
		if (add_cr == True):
			newfile.write(a+"\n")
		else:
			newfile.write(a)
	return

def readfile(name_of_file, cr = 1):
	#print "Loading "+name_of_file+"..."
	file_data = open(name_of_file)
	file_contents = file_data.readlines()
	output = []
	for i,line in enumerate(file_contents):
		if (i <> len(file_contents)-1): # no CR on last line, apparently
			output.append(line[:(-1* cr)]) # strip carriage returns
		else:
			output.append(line)
	return output

def joinslicesExplicit():
	# number_of_slices_to_do = int(sys.argv[2])
	d = ","
	header =  [','.join(['n','probe,symbol'] * max_combos_to_test) + d + 'Classification'] 
	output = []
	for file_number in range(number_of_slices_to_do):
		data = readfile(dir + "/" + "output_slice_" + str(file_number) + ".csv")
		if len(data) > 0:
			data[-1] = data[-1][:-1] # ugh, there is an EOF on the last line. Kludge.
			data = [a.split(',') for a in data]
			output += data

	output.sort(lambda x,y:cmp(float(y[-1]),float(x[-1]))) # sort by classification efficiency
	output = header + [','.join(a) for a in output]
	write_file(output, outfile, directory=dir, add_cr = True)
	
def joinslices():
	d = ","
	header =  [','.join(['n','probe,symbol'] * max_combos_to_test) + d + 'Classification'] 
	output = []
	# for file_number in range(number_of_slices_to_do):
	for infile in glob.glob( os.path.join(dir, '*.csv') ):
		print "current file is: " + infile
		data = readfile(infile)
		if len(data) > 0:
			data[-1] = data[-1][:-1] # ugh, there is an EOF on the last line. Kludge.
			data = [a.split(',') for a in data]
			output += data

	output.sort(lambda x,y:cmp(float(y[-1]),float(x[-1]))) # sort by classification efficiency
	output = header + [','.join(a) for a in output]
	write_file(output, outfile, directory=dir, add_cr = True)
	
dir = sys.argv[1]
outfile = sys.argv[2]
max_combos_to_test = int(sys.argv[3])

joinslices()

# join tdir 3 2 t.csv

