from .genotype import *
from .individual import *
from .family import *

# parsing function for csv file containing genotype data for families and populations
def parse_csv(stream, sep):
	"""Reads a CSV file and returns marker names, families, and genotypes.
	"""
	import csv
	reader = csv.reader(stream, delimiter = sep) # file object passed in
	line_iterator = iter(reader)
	
	# first line should be number of markers, indicator of presence of population name, indicator of presence of a subgroup name
	first_row = line_iterator.__next__()
	if len(first_row) < 3:
		raise CSVFileParseException(stream, 1, "Expecting at least three columns in the first row")

	marker_number = first_row[0]
	try:
		num_markers = int(marker_number)
	except:
		raise CSVFileParseException(stream, 1, 'Expecting the number of markers in the first cell of the first row (Found "%s")' % marker_number)

	pop_indicator = first_row[1]
	if pop_indicator == '1':
		pop_name = True
	elif pop_indicator == '0':
		pop_name = False
	else:
		raise CSVFileParseException(stream, 1, 'Expecting a 0 or 1 in the second column of the first row (Found "%s") to indicate population names absent or present' % pop_indicator)

	subgroup_indicator = first_row[2]
	if subgroup_indicator == '1':
		subgroup_name = True
		raise CSVFileParseException(stream, 1, 'Subgroup names not supported')
	elif subgroup_indicator == '0':
		subgroup_name = False
	else:
		raise CSVFileParseException(stream, 1, 'Expecting a 0 or 1 in the third column of the first row (Found "%s") to indicate subgroup names absent or present' % subgroup_indicator)

	second_row = line_iterator.__next__()
	if len(second_row) < num_markers:
		raise CSVFileParseException(stream, 2, "Expecting at least %s columns of marker names in the second row")
	# the lists within marker_names each contain two index positions, index 0 = marker name, index 1 = empty
	marker_names = []
	for n, marker in enumerate(second_row):
		if n >= num_markers:
			break
		if not marker.strip():
			raise CSVFileParseException(stream, 2, "Found an empty cell in column %d of line 2 (expected a marker name)" % (1 + n))
		marker_names.append([marker.strip(), []]) # add the marker names from the second row of the file to the list of marker names
	
	
	expected_column_number = 2 + 2*num_markers
	families_in_pop = {}
	for n, row in enumerate(line_iterator):
		if not row:
			continue # allow blank lines by skipping them
		if len(row) < expected_column_number:
			raise CSVFileParseException(stream, 3 + n, "Expecting at least %d columns, but found only" % (expected_column_number, len(row)))
		
		# the below code tags rows as containing either mom or offspring individuals
		population_name = row[1] # the population name is in the second cell of the row
		family_name = row[0] # the family name is in the first cell of the row
		if family_name.endswith('!'): # moms are indicated with an ! at the end of the family name
			mom = True
			family_name = family_name[0:-1] # the mom's family name is the text minus the !
		else:
			mom = False

		# puts family names in the name_to_fam dictionary
		# binds families to their population; family names (such as numeric values) can be reused without error
		key = (population_name, family_name)
		if key in families_in_pop:
			family = families_in_pop[key]
		else:
			family = Family(family_name)
			family.pop_name = population_name
			families_in_pop[key] = family

		assert population_name == family.pop_name

		offset = 2	# the first 2 columns in the csv file are not genotype data
		genotype_list = []
		for i in range(num_markers):
			first = None
			second = None
			
			# finds the first allele of a locus
			try:
				first = int(row[offset])
			except:
				if row[offset] != '?':
					raise CSVFileParseException(stream, 3 + n, "Expecting a number for an allele in column %d, but found %s" % (offset + 1, row[offset]))
			
			# finds the second allele of a locus
			try:
				second = int(row[offset + 1])
			except:
				if row[offset + 1] != '?':
					raise CSVFileParseException(stream, 3 + n, "Expecting a number for an allele in column %d, but found %s" % (offset + 2, row[offset + 1]))
			
			# constructs a multilocus genotype_list
			if (first is not None) and (second is not None):
				genotype_list.append(SingleLocusGenotype(first, second))
			else:
				genotype_list.append(None)
			alleles_per_locus = [first, second]
			info_for_this_locus = marker_names[i]
			info_for_this_locus[1] = (alleles_per_locus + info_for_this_locus[1])
			offset = offset + 2
		individual = Individual(family, genotype_list, mom)
	return marker_names, families_in_pop.values()	
    
class CSVFileParseException(Exception):
	"""Makes a CSVFileParseException class.
	"""
	def __init__(self, stream, line, msg):
		self.filename = stream.name
		self.line = line
		self.msg = msg
	
	def __str__(self):
		return "Error parsing %s at line %d:\n	%s\n" % (self.filename, self.line, self.msg)