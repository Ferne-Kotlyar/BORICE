import math

class Individual(object):
	"""An Individual object is a set of multilocus genotypes. Individuals belong to families, and are either an offspring or a mom of the family. Individuals also have inbreeding coefficients.
	"""
	def __init__(self, family, genotype_list, is_mom = False):
		self.family = family
		self.genotype_list = genotype_list
		self.inbreeding_coefficient = 0.0
		
		# designate individuals as either mom or offspring of a family
		if family is not None:
			if is_mom:
				family.add_mom(self)
			else:
				family.add_offspring(self)

	def __str__(self):
		"""Returns an individual's multilocus genotype as a string.
		"""
		x = "Genotype = ["
		for locus in self.genotype_list:
			x = x + str(locus) + ','
		return x + ']'
			
	def get_imputed_loci(self, population):
		"""Returns a list of genotypes that were imputed by def infer_mom or def tag_mom_genotype, and a list of the allele frequencies at each of those loci.
		"""
		imp = []
		alleles = []
		afreq = []
		for n, genotype in enumerate(self.genotype_list):
			allele_list = population.allele_list[n]
			allele_freq = population.allele_freq_list[n]
			if genotype == None:
				continue
			else:
				if (genotype.imputed == True) or (genotype.observed_imputed == True):
					imp.append(genotype)
					alleles.append(allele_list)
					afreq.append(allele_freq)
		assert len(imp) == len(alleles) == len(afreq)
		return imp, alleles, afreq
	
	def calc_inbreeding_coefficient(self, ih):
		"""Calculates the inbreeding coefficient (f) of an individual.
		"""
		assert (ih >= 0)
		if (ih >= 0) and (ih <= 5):
			self.inbreeding_coefficient = 1.0 - math.pow(0.5, ih)
		else:
			self.inbreeding_coefficient = 1.0
		return self.inbreeding_coefficient
	
	def calc_prob_offspring_geno(self, outcrossing_rate, population, mom, null_loci):
		"""Calculates an individual's multilocus genotype probability given its single-locus genotype probabilities.
		"""
		multilocus_selfing_prob = 1.0
		for n, genotype in enumerate(self.genotype_list):
			mom_g = mom.genotype_list[n]
			if mom_g == None:
				multilocus_selfing_prob = multilocus_selfing_prob * genotype.calc_prob_offspring_given_selfing_mom_homozygote_standard_model(mom_g, n)
			else:
				mf, ms = mom_g.first, mom_g.second
				mh = (mf == ms)
				null = null_loci[n]
				if null:
					if mh:
						multilocus_selfing_prob = multilocus_selfing_prob * genotype.calc_prob_offspring_given_selfing_mom_homozygote_null_model(mom_g, n)
					else:
						multilocus_selfing_prob = multilocus_selfing_prob * genotype.calc_prob_offspring_given_selfing_mom_heterozygote_null_model(mom_g, n)
				else:
					if mh:
						multilocus_selfing_prob = multilocus_selfing_prob * genotype.calc_prob_offspring_given_selfing_mom_homozygote_standard_model(mom_g, n)
					else:
						multilocus_selfing_prob = multilocus_selfing_prob * genotype.calc_prob_offspring_given_selfing_mom_heterozygote_standard_model(mom_g, n)
		
		#for testing only!
# 		for n, genotype in enumerate(self.genotype_list):
# 			mom_g = mom.genotype_list[n]
# 			mf, ms = mom_g.first, mom_g.second
# 			mh = (mf == ms)
# 			null = null_loci[n]
# 			if null:
# 				if mh:
# 					prob = genotype.calc_prob_offspring_given_selfing_mom_homozygote_null_model(mom_g, n)
# 				else:
# 					prob = genotype.calc_prob_offspring_given_selfing_mom_heterozygote_null_model(mom_g, n)
# 			else:
# 				if mh:
# 					prob = genotype.calc_prob_offspring_given_selfing_mom_homozygote_standard_model(mom_g, n)
# 				else:
# 					prob = genotype.calc_prob_offspring_given_selfing_mom_heterozygote_standard_model(mom_g, n)
# 			print("Genotype probability of selfing = %s" % prob)
# 			
		multilocus_outcrossing_prob = 1.0
		for n, genotype in enumerate(self.genotype_list):
			allele_list = population.allele_list[n]
			allele_freq = population.allele_freq_list[n]
			mom_g = mom.genotype_list[n]
			if mom_g == None:
				multilocus_outcrossing_prob = multilocus_outcrossing_prob * genotype.calc_prob_offspring_given_outcrossing_mom_homozygote_standard_model(allele_list, allele_freq, mom_g, n)
			else:
				mf, ms = mom_g.first, mom_g.second
				mh = (mf == ms)	
				null = null_loci[n]
				if null:
					if mh:
						multilocus_outcrossing_prob = multilocus_outcrossing_prob * genotype.calc_prob_offspring_given_outcrossing_mom_homozygote_null_model(allele_list, allele_freq, mom_g, n)
					else:
						multilocus_outcrossing_prob = multilocus_outcrossing_prob * genotype.calc_prob_offspring_given_outcrossing_mom_heterozygote_null_model(allele_list, allele_freq, mom_g, n)
				else:
					if mh:
						multilocus_outcrossing_prob = multilocus_outcrossing_prob * genotype.calc_prob_offspring_given_outcrossing_mom_homozygote_standard_model(allele_list, allele_freq, mom_g, n)
					else:
						multilocus_outcrossing_prob = multilocus_outcrossing_prob * genotype.calc_prob_offspring_given_outcrossing_mom_heterozygote_standard_model(allele_list, allele_freq, mom_g, n)
		
		#for testing only!
# 		for n, genotype in enumerate(self.genotype_list):
# 			allele_list = population.allele_list[n]
# 			allele_freq = population.allele_freq_list[n]
# 			mom_g = mom.genotype_list[n]
# 			mf, ms = mom_g.first, mom_g.second
# 			mh = (mf == ms)	
# 			null = null_loci[n]
# 			if null:
# 				if mh:
# 					prob = genotype.calc_prob_offspring_given_outcrossing_mom_homozygote_null_model(allele_list, allele_freq, mom_g, n)
# 				else:
# 					prob = genotype.calc_prob_offspring_given_outcrossing_mom_heterozygote_null_model(allele_list, allele_freq, mom_g, n)
# 			else:
# 				if mh:
# 					prob = genotype.calc_prob_offspring_given_outcrossing_mom_homozygote_standard_model(allele_list, allele_freq, mom_g, n)
# 				else:
# 					prob = genotype.calc_prob_offspring_given_outcrossing_mom_heterozygote_standard_model(allele_list, allele_freq, mom_g, n)
# 			print("Genotype probability of outcrossing = %s" % prob)
# 		
		selfing_rate = (1.0 - outcrossing_rate)
		prob_offspring_geno = (selfing_rate * multilocus_selfing_prob) + (outcrossing_rate * multilocus_outcrossing_prob)
		try:
			lnL = math.log(prob_offspring_geno)
		except:
			lnL = float('-inf')
		return lnL

	def calc_prob_mom_geno(self, population):
		"""Calculates a maternal individual's multilocus genotype probability given its single-locus genotype probabilities.
		"""
		multilocus_mom_prob = 1.0
		for n, genotype in enumerate(self.genotype_list):
			if genotype == None: # this is for the case where it is a single-offspring family with missing data and no maternal genotype
				multilocus_mom_prob = multilocus_mom_prob * 1.0
			else:
				allele_list = population.allele_list[n]
				allele_freq = population.allele_freq_list[n]
				multilocus_mom_prob = multilocus_mom_prob * genotype.calc_prob_mom(allele_list, allele_freq, self.inbreeding_coefficient)
		try:
			lnL = math.log(multilocus_mom_prob)
		except:
			lnL = float('-inf')
		return lnL