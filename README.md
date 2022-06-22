# GUIDE TO INSTALLATION & USE OF BORICE
BORICE is free software developed by Vanessa Koelling, Patrick Monnahan, and John Kelly (modified by Ferne Kotylar and Adrien Givry) to estimate the mean outcrossing rate and inbreeding coefficient of populations using Bayesian methods. To learn more about how this software works, its uses, and for the purposes of citing this software, please refer to the following publication:

	Koelling, V. A., P. J. Monnahan, and J. K. Kelly. 2012. A Bayesian method for the joint
	estimation of outcrossing rate and inbreeding depression. Heredity 109: 393-400. 
	doi:10.1038/hdy.2012.58

This version introduces several changes:
- Updated to work with Python 3 and PyQt5
- Updated documentation
- Added a toggle to ignore genotype errors
- Improved project structure
- New command-line argument parsing

## Quick Start
Skip this section if you want a detailed guide on how to install & run BORICE.
```properties
# Clone BORICE
git clone https://github.com/Ferne-Kotlyar/BORICE

# Change directory
cd BORICE

# Install BORICE
pip install -r requirements.txt
pip install -e .

# Run BORICE CLI with the default settings
python borice example_datafile.csv

# Run BORICE GUI
python borice_gui
```

## Requirements
BORICE was initially developed using Python 2.7. It has been updated to work with Python 3 (tested with 3.9.12), but should work with other versions of Python 3 as well.

Go to the following website to download Python: 

	http://www.python.org/download/

The installation guide bellow assumes that you are familiar with:
- [pip](https://pypi.org/project/pip/) (package installer for python)
- [CLI](https://en.wikipedia.org/wiki/Command-line_interface) (command-line interface, such as *terminal* on MacOS/Linux, and *Command Prompt* on Windows)

## Installation
Install BORICE requirements by typing this command:
```properties
pip install -r requirements.txt
```

You can then install the package by typing:
```properties
pip install -e .
```

## Usage
### BORICE CLI (for command-line users)
BORICE CLI is recommended for users who are familiar with command-line programs. BORICE CLI comes in handy when BORICE needs to be executed from another program (ex: running BORICE from an R script).

To run BORICE with the default settings, type the following command:
```properties
python borice example_datafile.csv
```
Replace `example_datafile.csv` with any CSV data file you want to work with (see data file formatting below).

BORICE CLI comes with a variety of settings. You can read about these options by typing:
```properties
python borice --help
```

### BORICE GUI (recommended)
As opposed to the CLI version, the GUI version of BORICE doesn't take any command-line arguments, instead, BORICE GUI lets you tweak its settings through a graphical user interface (GUI). To run BORICE GUI, you can type this command:
```properties
python borice_gui
```
Once BORICE GUI is open, you should see a blank screen. In the menu bar, click on "File", then "Open Data File"; select your input data file. A setting panel should appear where you can choose to edit BORICE's default parameters.

Click "Run" to start processing your data. You will get an alert message when the run is complete.

Settings for BORICE are separated into several tabs:

#### General Settings
|Setting|Default|Description|
|-|-|-|
|Number of Steps|`100000`|Number of steps taken in the MCMC chain. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the chain length is too short.|
|Number of Burn In Steps|`9999`|Number of initial steps that will be discarded before the posterior distributions are calculated. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the burn-in length is too short.|
|Outcrossing Rate Tuning Parameter|`0.05`|Determines how large a change in outcrossing rate is made at each step.|
|Allele Frequency Tuning Parameter|`0.1`|Determines how large a change in allele frequency is made at each step.|
|Initial Population Outcrossing Rate|`0.5`|Determines the starting outcrossing rate value for the chain.|
|Ignore Genotyping Errors|`False`|Skips any offspring that has an allele that does not match the mother if set to `True`.|

#### File Output Options
You also have the option of choosing the output files from your BORICE run under the “File Output Options” tab. The default settings are to produce all files. Output 1 is always produced; it contains the posterior distributions of t and F, population inbreeding history, and allele frequencies at each locus. Output 2 contains the posterior distributions of maternal inbreeding histories. Output 3 contains the list of t and F values from every 10 steps in the MCMC chain. Output 4 contains the posterior distributions for each maternal genotype at each locus in each family. These output files are tab-delimited text files that can be imported into spreadsheets.
Setting|Default|
|-|-|
|Posterior Distributions of Maternal Inbreeding Histories|`True`|
|List of t and F values|`True`|
|Posterior Distributions for each maternal genotype at each locus in each family|`True`|

#### Input Data Summary
The "Input Data Summary" tab shows you the number of marker loci, number of families, and number of individuals read from your input data file. If these numbers are not correct, then you should check your input data file.

#### Locus Settings
The "Locus Settings" tab allows you to choose whether to run each locus as having null alleles or not. The default setting is all boxes unchecked, which means null alleles will not be considered at a locus. Checking a locus box means null alleles will be considered at that locus. If you are uncertain whether or not to run BORICE with null alleles considered at a locus, you may want to try running BORICE with and without null alleles to compare the average ln likelihood. If you see a substantial improvement in the ln likelihood when running the model with null alleles at that locus, then null alleles may be present. In addition, BORICE makes an initial check of the data for impossible genotypes. If impossible genotypes are present at a locus even after you have checked your data for input errors, then null alleles may be present at that locus and you may wish to try the model with null alleles considered.
|Setting|Default|Description|
|-|-|-|
|Locus *n*|`True`|Considers null alleles at locus `n` if set to `True`|

## Data file format (CSV)
BORICE takes genotype data in the form of comma-separated value (CSV) files. In your csv file, missing data should be coded as `-9`.

### First Row
This row should contain the following in the first three cells:
1. the number of marker loci,
2. `0` or `1` to indicate the absence or presence of a population name in your data
3. `0` or `1` to indicate the absence or presence of a subgroup name in your data.
   
Currently, subgroups are not supported, so if subgroups are present they will be ignored.

*Example:*
```
3,1,0
```

### Second Row
The second row should contain the names of your marker loci.

*Example:*
```
aat374,aat240,aat367
```

### Following Rows
All other rows should be in the following format:
1. family name
2. population name (unless there isn't one)
3. allele 1 of marker locus 1
4. allele 2 of marker locus 1
5. [...] *and so forth for all loci.*

*Example:*
```
10,SS,152,152,98,98,-9,-9
```

If maternal individuals are present, they should be indicated with a `!` after the family name (*e.g., `fam1!`*).

### Example Data File
```csv
3,1,0,,,,,
aat374,aat240,aat367,,,,,
10!,SS,152,152,98,98,-9,-9
10,SS,149,149,98,98,185,191
10,SS,149,149,98,98,191,191
10,SS,149,149,98,98,185,191
100!,SS,149,152,98,98,185,185
100,SS,149,149,98,98,185,185
100,SS,149,152,98,98,185,185
100,SS,149,152,98,98,188,188
12!,SS,149,149,98,98,185,191
12,SS,149,152,98,98,185,191
12,SS,149,152,98,98,185,191
12,SS,152,152,-9,-9,-9,-9
14!,SS,149,149,98,98,185,185
```

## Output Files
BORICE generates 4 output files. The first one (Output 1) is always generated, the rest are optional.

|Generated File|Description|
|-|-|
|Output 1|Posterior Distribution of Population Inbreeding History|
|Output 2|Posterior Distributions of Maternal Inbreeding Histories|
|Output 3|List of t and F values|
|Output 4|Posterior Distributions for each maternal genotype at each locus in each family|

## Unit Tests
BORICE has been setup to use [PyTest](https://pytest.org). You can run BORICE unit tests with the following command:
```properties
pytest
```