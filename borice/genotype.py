import math
import random

def tag_mom_genotype(momfirst, momsecond, offspring, locus_index, null_loci, family, ignore_genotyping_errors):
	"""Tags an observed maternal genotype as imputed if it is a homozygote, and returns a SingleLocusGenotype. This is for the purpose of dealing with null alleles.
	"""
# #	for testing only when moms need to be read in as is!
#  	slg = SingleLocusGenotype(momfirst, momsecond)
#  	slg.imputed = True
#  	return slg
	
	m_list = [momfirst, momsecond]
	works = True
	for child in offspring:
		cg = child.genotype_list[locus_index]
		# skips missing genotypes
		if ignore_genotyping_errors or ((cg.first == -9) and (cg.second == -9)):
			continue
		# checks that the observed genotype is possible based on the progeny genotype
		if (cg.first not in m_list) and (cg.second not in m_list):
			works = False
			break
	
	null = null_loci[locus_index]
	if null:
		if works:
			if (momfirst == momsecond):
				slg = SingleLocusGenotype(momfirst, momsecond)
				slg.observed_imputed = True
				return slg
			else:
				slg = SingleLocusGenotype(momfirst, momsecond)
				return slg
		else:
			if (momfirst == momsecond):
				null_allele = 0
				momfirst = null_allele
				m_list = [momfirst, momsecond]
				works = True
				for child in offspring:
					cg = child.genotype_list[locus_index]
					# skips missing genotypes
					if ignore_genotyping_errors or ((cg.first == -9) and (cg.second == -9)):
						continue
					# checks that imputed null genotype is possible based on progeny genotype
					if (cg.first == cg.second):
						if (cg.first not in m_list) and (null_allele not in m_list):
							works = False
							break
					else:
						if (cg.first not in m_list) and (cg.second not in m_list):
							works = False
							break
				if works:
					slg = SingleLocusGenotype(momfirst, momsecond)
					slg.observed_imputed = True
					return slg
				else:
					raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)
			else:
				if (momfirst == 0):
					null_allele = 0
					m_list = [momfirst, momsecond]
					works = True
					for child in offspring:
						cg = child.genotype_list[locus_index]
						# skips missing genotypes
						if ignore_genotyping_errors or ((cg.first == -9) and (cg.second == -9)):
							continue
						# checks that null heterozygote genotype is possible based on progeny genotype
						if (cg.first == cg.second):
							if (cg.first not in m_list) and (null_allele not in m_list):
								works = False
								break
						else:
							if (cg.first not in m_list) and (cg.second not in m_list):
								works = False
								break
					if works:
						slg = SingleLocusGenotype(momfirst, momsecond)
						return slg
					else:
						raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)
				else:
					raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)
	else:
		if works:
			slg = SingleLocusGenotype(momfirst, momsecond)
			return slg
		else:
			raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)

def find_mom_genotype(allele_set, offspring, locus_index, null_loci, family, valid_geno_index = 0):
	"""Imputes a maternal genotype, tags it as imputed, and returns a SingleLocusGenotype.
	"""
	# selects the first maternal genotype that works for the family
	null = null_loci[locus_index]
	if null:
		null_allele = 0
		for momfirst in allele_set:
			for momsecond in allele_set:
				m_list = [momfirst, momsecond]
				works = True
				for child in offspring:
					cg = child.genotype_list[locus_index]
					# skips missing genotypes
					if (cg.first == -9) and (cg.second == -9):
						continue
					# checks that imputed genotype is possible based on progeny genotype
					if (cg.first == cg.second):
						if (cg.first not in m_list) and (null_allele not in m_list):
							if valid_geno_index == 0:
								works = False
								break
							else:
								valid_geno_index = valid_geno_index - 1
					else:
						if (cg.first not in m_list) and (cg.second not in m_list):
							if valid_geno_index == 0:
								works = False
								break
							else:
								valid_geno_index = valid_geno_index - 1
				if works:
					slg = SingleLocusGenotype(momfirst, momsecond)
					slg.imputed = True
					return slg
		
		if works:
			pass
		else:
			raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)
	else:
		for momfirst in allele_set:
			for momsecond in allele_set:
				m_list = [momfirst, momsecond]
				works = True
				for child in offspring:
					cg = child.genotype_list[locus_index]
					# skips missing genotypes
					if (cg.first == -9) and (cg.second == -9):
						continue
					# checks that imputed genotype is possible based on progeny genotype
					if (cg.first not in m_list) and (cg.second not in m_list):
						if valid_geno_index == 0:
							works = False
							break
						else:
							valid_geno_index = valid_geno_index - 1
				if works:
					slg = SingleLocusGenotype(momfirst, momsecond)
					slg.imputed = True
					return slg
		if works:
			pass
		else:
			raise SingleLocusGenotypeError(cg.first, cg.second, locus_index, family)

class SingleLocusGenotypeError(Exception):
	"""Makes a SingleLocusGenotypeError class. If an impossible genotype is encountered in the data, it prints the genotype and identifies the family in which it occurs.
	"""
	def __init__(self, first, second, locus, family):
		self.first = first
		self.second = second
		self.locus_number = locus
		self.family = family
		
	def __str__(self):
		return "Impossible genotype %s/%s at locus %s in family %s!" % (self.first, self.second, self.locus_number + 1, self.family)
        
class SingleLocusGenotype(object):
	"""A SingleLocusGenotype is an object made up of two alleles, 'first' and 'second'. Alleles in a genotype are ordered smallest (first) to largest (second).
	"""
	def __init__(self, first, second):
		self.first = min(first, second)
		self.second = max(first, second)
		self.imputed = False
		self.observed_imputed = False
		
	def __str__(self):
		"""Returns a genotype string with the first and second alleles separated by a slash.
		"""
		return repr(self.first) + '/' + repr(self.second)
	
	def calc_prob_offspring_given_selfing_mom_homozygote_standard_model(self, mom_g, locus):
		"""Calculates the probability of a homozygous offspring genotype given selfing and its maternal genotype; no null alleles, no allelic drop-out.
		"""
		if mom_g == None: # this is the case for a single-offspring family with no maternal genotype missing data at this locus; effectively skips the locus
			return 1.0
		else:
			mf = mom_g.first
			sf, ss = self.first, self.second
			sh = (sf == ss)
			if (sf == -9) and (ss == -9): # missing data; effectively skips the locus
				return 1.0
			else:
				if sh and (sf == mf): # offspring is homozygous
					return 1.0
				else: # impossible genotype
					return 0.0

	def calc_prob_offspring_given_selfing_mom_homozygote_null_model(self, mom_g, locus):
		"""Calculates the probability of a homozygous offspring genotype given selfing and its maternal genotype with null alleles.
		"""
		mf = mom_g.first
		sf, ss = self.first, self.second
		sh = (sf == ss)
		if (sf == -9) and (ss == -9): # missing data; effectively skips the locus
			return 1.0
		else:
			if (mf == 0): # mom is homozygous null
				return 0.0
			else: # mom is not homozygous null
				if sh: # offspring is homozygous
					if (sf == mf):
						return 1.0
					else: # impossible genotype
						return 0.0
				else: # offspring is het
					return 0.0
	
	def calc_prob_offspring_given_selfing_mom_heterozygote_standard_model(self, mom_g, locus):
		"""Calculates the probability of a heterozygous offspring genotype given selfing and its maternal genotype; no null alleles, no allelic drop-out.
		"""
		if mom_g == None: # this is the case for a single-offspring family with no maternal genotype missing data at this locus; effectively skips the locus
			return 1.0
		else:
			mf, ms = mom_g.first, mom_g.second
			sf, ss = self.first, self.second
			sh = (sf == ss)
			if (sf == -9) and (ss == -9): # missing data
				return 1.0
			elif (sf != mf) and (sf != ms) and (ss != mf) and (ss != ms): # impossible genotype
				return 0.0
			elif sh: # offspring is homozygous
				return 0.25
			elif (sf == mf) and (ss == ms): # offspring is identical het
				return 0.5
			else: # offspring is non-identical het
				return 0.0

	def calc_prob_offspring_given_selfing_mom_heterozygote_null_model(self, mom_g, locus):
		"""Calculates the probability of a heterozygous offspring genotype given selfing and its maternal genotype with null alleles.
		"""
		mf, ms = mom_g.first, mom_g.second
		sf, ss = self.first, self.second
		sh = (sf == ss)
		if (sf == -9) and (ss == -9): # missing data
			return 1.0
		else:
			if (mf == 0): # mom is het with null allele	
				if sh and (sf == ms): # offspring is homozygous and not null
					return 1.0
				else: # impossible genotype
					return 0.0
			else: # mom is het without null allele
				if (sf != mf) and (sf != ms) and (ss != mf) and (ss != ms): # impossible genotype
					return 0.0
				elif sh: # offspring is homozygous
					return 0.25
				elif (sf == mf) and (ss == ms): # offspring is identical het
					return 0.5
				else: # offspring is non-identical het
					return 0.0
	
	def calc_prob_offspring_given_outcrossing_mom_homozygote_standard_model(self, allele_list, allele_freq, mom_g, locus):
		"""Calculates the probability of a homozygous offspring genotype given outcrossing and its maternal genotype; no null alleles, no allelic drop-out.
		"""
		if mom_g == None: # this is the case for a single-offspring family with no maternal genotype missing data at this locus; effectively skips the locus
			return 1.0
		else:
			mf, ms = mom_g.first, mom_g.second
			sf, ss = self.first, self.second
		
			# missing data (-9) is not in the allele list and must be skipped
			if (sf == -9) and (ss == -9):
				return 1.0
			else:
				allele1 = allele_list.index(sf)
				allele2 = allele_list.index(ss)

			if (sf == mf):
				return allele_freq[allele2]
			elif (ss == mf):
				return allele_freq[allele1]
			else: # impossible genotype
				return 0.0

	def calc_prob_offspring_given_outcrossing_mom_homozygote_null_model(self, allele_list, allele_freq, mom_g, locus):
		"""Calculates the probability of a homozygous offspring genotype given outcrossing and its maternal genotype with null alleles.
		"""
		mf, ms = mom_g.first, mom_g.second
		sf, ss = self.first, self.second
		sh = (sf == ss)
		null_allele = allele_list.index(0)
		
		# missing data (-9) is not in the allele list and must be skipped
		if (sf == -9) and (ss == -9):
			return 1.0
		else:
			allele1 = allele_list.index(sf)
			allele2 = allele_list.index(ss)
		
		if (mf == 0): # mom is homozygous null
			if sh: # offspring is homozygous
				return (allele_freq[allele1])/(1.0 - allele_freq[null_allele])
			else: # offspring is het
				return 0.0
		else: # mom is homozygous not null
			if sh: # offspring is homozygous
				if (sf == mf):
					return (allele_freq[allele1] + allele_freq[null_allele])
				else: # impossible genotype
					return 0.0
			else: # offspring is het
				if (sf == mf):
					return allele_freq[allele2]
				elif (ss == mf):
					return allele_freq[allele1]
				else: # impossible genotype
					return 0.0
	
	def calc_prob_offspring_given_outcrossing_mom_heterozygote_standard_model(self, allele_list, allele_freq, mom_g, locus):
		"""Calculates the probability of a heterozygous offspring genotype given outcrossing and its maternal genotype; no null alleles, no allelic drop-out.
		"""
		if mom_g == None: # this is the case for a single-offspring family with no maternal genotype missing data at this locus; effectively skips the locus
			return 1.0
		else:
			mf, ms = mom_g.first, mom_g.second
			sf, ss = self.first, self.second
			sh = (sf == ss)
		
			# missing data (-9) is not in the allele list and must be skipped
			if (sf == -9) and (ss == -9):
				return 1.0
			else:
				allele1 = allele_list.index(sf)
				allele2 = allele_list.index(ss)
		
			if sh: # offspring is homozygote
				if (sf == mf):
					return allele_freq[allele1] * 0.5
				elif (sf == ms):
					return allele_freq[allele2] * 0.5
				else: # impossible genotype
					return 0.0
			else: # offspring is het
				if (sf != mf) and (sf != ms) and (ss != mf) and (ss != ms): # impossible genotype
					return 0.0
				elif (sf != mf) and (sf != ms):
					return allele_freq[allele1] * 0.5
				elif (ss != mf) and (ss != ms):
					return allele_freq[allele2] * 0.5
				else: # offspring is identical het
					return 0.5 * (allele_freq[allele1] + allele_freq[allele2])

	def calc_prob_offspring_given_outcrossing_mom_heterozygote_null_model(self, allele_list, allele_freq, mom_g, locus):
		"""Calculates the probability of a heterozygous offspring genotype given outcrossing and its maternal genotype with null alleles.
		"""
		mf, ms = mom_g.first, mom_g.second
		sf, ss = self.first, self.second
		sh = (sf == ss)
		null_allele = allele_list.index(0)
		
		# missing data (-9) is not in the allele list and must be skipped
		if (sf == -9) and (ss == -9):
			return 1.0
		else:
			allele1 = allele_list.index(sf)
			allele2 = allele_list.index(ss)
		
		if (mf == 0): # mom is het with null allele
			if sh:
				if (sf == ms): # offspring is homozygote and matches maternal allele 2
					return (allele_freq[allele1]/(1.0 - allele_freq[null_allele]) * 0.5) + ((allele_freq[allele1] + allele_freq[null_allele]) * 0.5)
				else: # offspring is homozygote and does not match maternal allele 2
					return allele_freq[allele1]/(1.0 - allele_freq[null_allele]) * 0.5
			else: # offspring is het
				if (sf == ms):
					return allele_freq[allele2] * 0.5
				elif (ss == ms):
					return allele_freq[allele1] * 0.5
				else: # impossible genotype
					return 0.0
		else: # mom is het without null allele
			if sh: # offspring is homozygous
				if (sf == mf):
					return (allele_freq[allele1] + allele_freq[null_allele]) * 0.5
				elif (sf == ms):
					return (allele_freq[allele1] + allele_freq[null_allele]) * 0.5
				else: # impossible genotype
					return 0.0
			else: # offspring is het
				if (sf != mf) and (sf != ms) and (ss != mf) and (ss != ms): # impossible genotype
					return 0.0
				elif (sf != mf) and (sf != ms):
					return allele_freq[allele1] * 0.5
				elif (ss != mf) and (ss != ms):
					return allele_freq[allele2] * 0.5
				else: # offspring is identical het
					return 0.5 * (allele_freq[allele1] + allele_freq[allele2])

	def calc_prob_mom(self, allele_list, allele_freq, inbreeding_coefficient):
		"""Calculates the probability of a maternal genotype given its inbreeding coefficient.
		"""
		sf, ss = self.first, self.second
		sh = (sf == ss)
		allele1 = allele_list.index(sf)
		allele2 = allele_list.index(ss)
		inb = (1.0 - inbreeding_coefficient)
		if sh:
			return (inb * math.pow(allele_freq[allele1], 2)) + (inbreeding_coefficient * allele_freq[allele1])
		else:
			return (inb * (2.0 * allele_freq[allele1] * allele_freq[allele2]))
				
	def impute_new_mom(self, allele_list, allele_freq, inbreeding_coefficient, locus, null_loci):
		"""Selects a new maternal genotype based on allele frequencies if there is no observed genotype at this locus. If the maternal genotype is an observed homozygote at this locus, a choice is made whether or not to step from the current genotype (homozygote or null heterozygote) based on the probability of those genotypes.
		"""
		assert round(sum(allele_freq), 1) == 1.0
		
		sf, ss = self.first, self.second
		sh = (sf == ss)
		
		if self.imputed:
			rand_num = random.random()
			cumulative_prob = 0
			i = 0
			null = null_loci[locus]
			if null:
				first_allele = 0
			else:
				first_allele = 1 # skip allele zero, which is at frequency 0.0
			# choose first allele
			while i == 0:
				cumulative_prob = cumulative_prob + allele_freq[first_allele]
				if rand_num < cumulative_prob:
					new_first = allele_list[first_allele]
					i = 1
				else:
					first_allele = first_allele + 1
		
			# choose second allele
			r_number = random.random()
			if r_number < inbreeding_coefficient:
				# mom is new homozygote
				new_second = new_first
			else:
				random_number = random.random()
				cum_prob = 0
				j = 0
				if null:
					second_allele = 0
				else:
					second_allele = 1 # skip allele zero, which is at frequency 0.0
				while j == 0:
					# mom is new het
					cum_prob = cum_prob + allele_freq[second_allele]
					if random_number < cum_prob:
						new_second = allele_list[second_allele]
						j = 1
					else:
						second_allele = second_allele + 1
		
			j = new_first
			k = new_second
			new_first = min(j, k)
			new_second = max(j, k)
		else:
			if self.observed_imputed: # this should only be true when the mom is an observed homozygote
				null_allele = allele_list.index(0)
				allele = allele_list.index(ss)
				r_num = random.random()
				inb = (1.0 - inbreeding_coefficient)
				if sh: # current genotype is same as observed homozygote
					null_het_prob = inb * (2.0 * allele_freq[allele] * allele_freq[null_allele]) # prob of null het
					if r_num < null_het_prob:
						new_first = 0
						new_second = ss
					else:
						new_first = sf
						new_second = ss
				else: # current genotype is null heterozygote alternative to observed homozygote
					homozygote_prob = (inb * math.pow(allele_freq[allele], 2)) + (inbreeding_coefficient * allele_freq[allele]) # prob of homozygote
					if r_num < homozygote_prob:
						new_first = ss
						new_second = ss
					else:
						new_first = sf
						new_second = ss
		return new_first, new_second