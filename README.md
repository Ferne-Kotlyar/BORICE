# GUIDE TO INSTALLATION & USE OF BORICE: BAYESIAN OUTCROSSING RATE AND INBREEDING COEFFICIENT ESTIMATION SOFTWARE
BORICE is free software developed by Vanessa Koelling, Patrick Monnahan, and John Kelly to estimate the mean outcrossing rate and inbreeding coefficient of populations using Bayesian methods. To learn more about how this software works, its uses, and for the purposes of citing this software, please refer to the following publication:

	Koelling, V. A., P. J. Monnahan, and J. K. Kelly. 2012. A Bayesian method for the joint
	estimation of outcrossing rate and inbreeding depression. Heredity 109: 393-400. 
	doi:10.1038/hdy.2012.58

This version introduces several changes:
- Updated to work with Python 3 and PyQt5
- Updated documentation
- Added a toggle to ignore genotype errors

## How To Format Your Data Files for Use with BORICE
BORICE takes genotype data in the form of comma-separated value (csv) files. In your csv file, missing data should be coded as '-9'. The first row of the csv file should contain the following in the first three cells: 1) the number of marker loci, 2) a 0 or 1 to indicate the absence or presence of a population name in your data, and 3) a 0 or 1 to indicate the absence or presence of a subgroup name in your data. Currently, subgroups are not supported, so if subgroups are present they will be ignored. The second row should contain the names of your marker loci. All other rows should be in the following format: cell 1 = family name; cell 2 = population name (unless there isn't one); cell 3 = allele 1 of marker locus 1; cell 4 = allele 2 of marker locus 1; and so forth for all loci. If maternal individuals are present, they should be indicated with a '!' after the family name (e.g., 'fam1!').

### Example Data File
	3,1,0,,,,,
	aat374,aat240,aat367,,,,,
	10,SS,152,152,98,98,-9,-9
	10,SS,149,149,98,98,185,191
	10,SS,149,149,98,98,191,191
	10,SS,149,149,98,98,185,191
	100,SS,149,152,98,98,185,185
	100,SS,149,149,98,98,185,185
	100,SS,149,152,98,98,185,185
	100,SS,149,152,98,98,188,188
	12,SS,149,149,98,98,185,191
	12,SS,149,152,98,98,185,191
	12,SS,149,152,98,98,185,191
	12,SS,152,152,-9,-9,-9,-9
	14,SS,149,149,98,98,185,185

## Dependencies
### Python
BORICE was initially developed using Python 2.7. It has updated to work with Python 3 (tested with 3.9.12), but should work with other versions of Python 3 as well.

Go to the following website to download Python: 

	http://www.python.org/download/

BORICE functions through a graphical user interface (GUI). In order for the GUI to function, you will need to install some additional third party software.

### PyQt5
You will need to install PyQt5, it can be found at the following website:

	https://pypi.org/project/PyQt5/

## How To Run 
To run BORICE GUI, open main.py from your BORICE folder. To do this from the terminal, execute this command: 

	python main.py

The “.py” denotes that this is a Python file. A Python window will then open labeled “BORICE”. The Command Prompt window will also be launched. Any errors that occur during the run will appear in the Command Prompt window.

Once BORICE GUI is open, click on the file menu and select “Open Data File”. Then select your input data file. You will then have the option to run BORICE with default settings or to change the settings. Below are the default settings listed under the “General Settings” tab.

### Default Settings
|Setting|Default Value|Description|
|-|-|-|
|Number of Steps|100000|The number of steps is the number of steps taken in the MCMC chain. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the chain length is too short.|
|Number of Burn In Steps|9999|The number of burn in steps is the number of initial steps that will be discarded before the posterior distributions are calculated. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the burn-in length is too short.|
|Outcrossing Rate Tuning Parameter|0.5|The outcrossing rate tuning parameter is the value that determines how large a change in outcrossing rate is made at each step.|
|Allele Frequency Tuning Parameter|0.1|The allele frequency tuning parameter is the value that determines how large a change in allele frequency is made at each step.|
|Initial Population Outcrossing Rate|0.5|The initial population outcrossing rate is the starting outcrossing rate value for the chain.|
|Ignore Genotyping Errors|False|If true, BORICE skips any offspring that has an allele that does not match the mother.|

### File Output Options
You also have the option of choosing the output files from your BORICE run under the “File Output Options” tab. The default settings are to produce all files. Output 1 is always produced; it contains the posterior distributions of t and F, population inbreeding history, and allele frequencies at each locus. Output 2 contains the posterior distributions of maternal inbreeding histories. Output 3 contains the list of t and F values from every 10 steps in the MCMC chain. Output 4 contains the posterior distributions for each maternal genotype at each locus in each family. These output files are tab-delimited text files that can be imported into spreadsheets.

### Input Data Check
The “Input Data Summary” tab shows you the number of marker loci, number of families, and number of individuals read from your input data file. If these numbers are not correct, then you should check your input data file.

### Locus Settings
The “Locus Settings” tab allows you to choose whether to run each locus as having null alleles or not. The default setting is all boxes unchecked, which means null alleles will not be considered at a locus. Checking a locus box means null alleles will be considered at that locus. If you are uncertain whether or not to run BORICE with null alleles considered at a locus, you may want to try running BORICE with and without null alleles to compare the average ln likelihood. If you see a substantial improvement in the ln likelihood when running the model with null alleles at that locus, then null alleles may be present. In addition, BORICE makes an initial check of the data for impossible genotypes. If impossible genotypes are present at a locus even after you have checked your data for input errors, then null alleles may be present at that locus and you may wish to try the model with null alleles considered.

### Running the Program
Click “Run” to run BORICE. If you do not see the prompt in the Command or Terminal window, BORICE is running. You will get an alert message when the run is complete.
