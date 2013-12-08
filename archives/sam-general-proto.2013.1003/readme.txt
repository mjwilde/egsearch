
1. User selects three files:

database (this is specific to the expression platform. It defines the metadata for each gene)
samples (these are the clinical samples and the descriptions of each) [Phenotype data]
data (the actual gene expression data) [Genotype data]

2. The program displays the header row of the samples and lets the user select the column with the class they want to use (e.g. alive vs. dead, age, etc.)

3. The user then defines the classes (e.g. alive vs. dead, age<100 vs. age>200). Restrict to two classes for now. The choices can be discrete (alive/dead) or continuous (age).

4. User defines which column in the database file corresponds to the feature column in the data. e.g is the gene column in the data file is probe number, then the probe number column from the database file will be chosen.

5. User defines the numbers of genes to test and how many ranked features. 
e.g. (3, 100) = all combinations of 3 from the top 100
(2, all) = all combinations of 2 (will need to get the total number from the data file, e.g. 35,000)
Tell the person how many combinations.

    n!
----------
(n-r)!(r!)

where n = number to choose from (e.g. 100) and r = number chosen (e.g. 2 or 3)

The output should be:

Dictionary for database, keys are unique gene identifier, values are the rest of the information
Dictionary for samples, keys are unique sample identifier, values are rest of the information
Array for the data where first column has the features (genes) and the top row has the samples.

