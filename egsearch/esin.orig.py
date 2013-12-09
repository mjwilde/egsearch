import os
import sys
import re

#read 2007 excel files

def average(somelist):
    if len(somelist)>0:
        return float(sum(somelist))/float(len(somelist))
    else:
        return 0.0


def readfile(name_of_file,cr = 1):       #read csv files
    file_data = open(name_of_file)
    file_contents = file_data.readlines()
    output = []
    for i,line in enumerate(file_contents):
        if (i <> len(file_contents)-1): # no CR on last line, apparently
            output.append(line[:(-1* cr)]) # strip carriage returns
        else:
            output.append(line)
    output = [a.split(',') for a in output]
    return output


def unique(s):
    n = len(s)
    if n == 0:
        return []
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u



def fabo(num): # factorial
    if num>1:
        res =num *fabo(num-1)
    else:
        res =num
    return res


def geneclassifier():

    test = True

    if not test:
        databasefilename = raw_input("Enter the Database file name:")
        samplefilename = raw_input("Enter the Sample file name:")
        datafilename = raw_input("Enter the Data file name:")
    else:
        databasefilename = "./database.csv"
        samplefilename = "./samples.csv"
        datafilename = "./data.csv"
    print databasefilename
    print samplefilename
    print datafilename

    sampledata = readfile(samplefilename)
    database = readfile(databasefilename)
    data = readfile(datafilename)

    classnames = ["discrete","continuous"]

    print "Column names of Sample file "
    #samplecolumnnames = sampledata[0].split(',') # assumes samples names in first row
    samplecolumnnames = sampledata[0]
    for n,column in enumerate(samplecolumnnames):
        print n,column

    if not test:
        columnindex = raw_input("Select the number corresponding to the column names (class name) which you want use: ")
    else:
        columnindex = 1
    print "You have selected:", samplecolumnnames[int(columnindex)]

    coldata = unique([a[columnindex] for a in sampledata[1:]])
    print "Data in that column:", coldata


    if not test:
        classdefined = raw_input("Is the selected class, 0 (discrete) or 1 (continuous)?")
        classdefined = int(classdefined)
    else:
        classdefined = 0

    if classdefined == 0 and not test:
        conditions = raw_input("List two conditions separated by a comma. e.g. 'Alive,Dead'")
        conditions = conditions.split(',')
    elif classdefined == 0 and test:
        conditions = "Alive,Dead"
        conditions = conditions.split(',')
    elif classdefined == '1' and not test:
        conditions = raw_input("List two functions used to define two classes. e.g. '<50,>100'")
    else:
        exit()
    print "Conditions:",conditions

    traininglabels = [0 if a == conditions[0] else 1 for a in [b[columnindex] for b in sampledata[1:]]]

    for i,c in enumerate(conditions):
        print i,c





    print "Here is a bit of your data from the first column"
    for line in data[0:5]:
        print line[0]

    print
    print"And here are the column headers for your database."
    for i,c in enumerate(database[0]):
        print i,c

    if not test:
        sampledefined = int(raw_input("Enter the number of the databaes column corresponding to the first column of your data"))
    else:
        sampledefined = 2




    exit()

    sampledic = {}
    sampledic['columnind'] = []
    sampledic['columnname'] = []
    sampledic['ind'] = []
    sampledic['classname'] = []

    for i,ind in enumerate(classindexes):
        sampledic['columnind'].append(colindexes[i])
        sampledic['columnname'].append(samplecolumnnames[int(colindexes[i])])
        sampledic['ind'].append(classindexes[i])
        sampledic['classname'].append(classnames[int(classindexes[i])])

    print "\nFeature column in data file:"
    for i,line in enumerate(data):
        print i,line.split(',')[0]

    print "\nColumn names and first row in database file:\n\n"+"Column names: "+database[0]+"\n"+"First row: "+database[1]
    selcolnum =raw_input("Define which column in database corresponds to the feature column in the data file,count from 1:")
    print "You selected column number: "+ selcolnum,",corresponds to column name: "+data[0].split(',')[int(selcolnum)-1] #int(selcolnum)-1
    userdefine =raw_input("Defines the numbers of genes to test and how many ranked features,example \"3,100\" or \"3,all\" :")
    print userdefine
    r = int(userdefine.split(',')[0])
    nn = userdefine.split(',')[1]
    #print  r,nn
    if nn=="all":
        nn=len(data)-1
    else:
        nn=int(nn)
    print "Selected gene number is ",nn
    selections =fabo(nn)/(fabo(nn-r)*fabo(r))
    print "There are "+str(selections)+" combinations."

    #output sampledic,Dictionary for database, keys are unique gene identifier, values are the rest of the information
    #Dictionary for samples, keys are unique sample identifier, values are rest of the information
    #Array for the data where first column has the features (genes) and the top row has the samples.

    sample ={}
    for i,line in enumerate(sampledata):
        if i>=0:
            units=line.split(',')
            sample[units[0]] =units[1:len(units)]

#        print len(sample[units[0]]),sample[units[0]][0],units[0]
 #       print sample.keys()[0],sample[sample.keys()[0]][0],sample[sample.keys()[0]][1],sample[sample.keys()[0]][2],sample[sample.keys()[0]][3]
    #print sample.keys()[1],sample[sample.keys()[1]][0],sample[sample.keys()[1]][1],sample[sample.keys()[1]][2],sample[sample.keys()[1]][3]

    databasedic ={}
    for i,line in enumerate(database):
        if i>=0:
            units=line.split(',')
            databasedic[units[0]] =units[1:len(units)]
  #      print databasedic.keys()[0],databasedic[databasedic.keys()[0]][0],databasedic[databasedic.keys()[0]][1],databasedic[databasedic.keys()[0]][2]


    dataarray=[]
    for i in xrange(len(data[0].split(','))):
        dataarray.append([])

    for i,line in enumerate(data):
        sline =line.split(',')
        for j,unit in enumerate(sline):
            dataarray[j].append(unit)



    #return sampledic(user define sample columns class), sample(sample data dictionary),databasedic(database dictionary),dataarray(array of data file)
    return  sampledic,sample,databasedic,dataarray


def printplus(obj):
    """
    Pretty-prints the object passed in.

    """
    # Dict
    if isinstance(obj, dict):
        for k, v in sorted(obj.items()):
            print u'{0}: {1}'.format(k, v)

    # List or tuple
    elif isinstance(obj, list) or isinstance(obj, tuple):
        for x in obj:
            print x

    # Other
    else:
        print obj

# Main code
getdictionary =geneclassifier()
sample =getdictionary[0]
sampledic =getdictionary[1]
databasedic =getdictionary[2]

# print out user defined sample  cloumns class, sample dictionary,database dictionary
print "User defined sample cloumns class:"
printplus(sample)
print "Sample data dictionary:"
printplus(sampledic)
print  "Database dictioinary:"
printplus(databasedic)
dataarray =getdictionary[3]
#print out the DATA arrayy
print "Data file:\n"
for i in xrange(len(dataarray[0])):
    print "\n"
    for j in xrange(len(dataarray)):
        print dataarray[j][i]
