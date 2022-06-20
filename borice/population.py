import math

class Population(object):
	"""A Population object consists of multiple families. Each population also has a list of allele frequencies specific to that population, as well as an outcrossing rate.
	"""
	def __init__(self, allele_list, allele_freq_list, y_values, outcrossing_rate):
		self.allele_list = allele_list
		self.allele_freq_list = allele_freq_list
		self.family_list = []
		self.outcrossing_rate = float(outcrossing_rate)
		self.ih_prob_list = []
		self.y_values = y_values
	
	def calculate_new_af_list(self, locus_alleles, locus_index, step, burn_in, null_loci):
		"""Calculates a new list of allele frequencies at a locus based on the y-value of each allele.
		"""
		null = null_loci[locus_index]
		if null:
			for n, allele in enumerate(locus_alleles):
				self.y_values[locus_index].append(allele.y)
			
			new_af_list = []
			for n, allele in enumerate(locus_alleles):
				new_af = allele.y / sum(self.y_values[locus_index])
				new_af_list.append(new_af)
				if step > burn_in:
					if (step % 10) == 0:
						allele.af_list.append(new_af)
		else:
			for n, allele in enumerate(locus_alleles):
				if n == 0:
					continue
				else:
					self.y_values[locus_index].append(allele.y)
			
			new_af_list = [0.0]
			for n, allele in enumerate(locus_alleles):
				if n == 0:
					continue
				else:
					new_af = allele.y / sum(self.y_values[locus_index])
					new_af_list.append(new_af)
					if step > burn_in:
						if (step % 10) == 0:
							allele.af_list.append(new_af)
		return new_af_list
	
	def calc_pop_lnL(self, null_loci):
		"""Calculates the ln likelihood of a population summed over families.
		"""
		lnL = 0.0
		for family in self.family_list:
			lnL = lnL + family.calc_family_lnL(self.outcrossing_rate, null_loci)
		return lnL
		
	def calc_ih_prob(self):
		"""Calculates a list of inbreeding history probabilities based on the population outcrossing rate.
		"""
		outcrossing_rate = self.outcrossing_rate
		for ih in range(0,7):
			if ih == 0:
				ih_prob = outcrossing_rate
				self.ih_prob_list.append(ih_prob)
			else:
				if (ih > 0) and (ih < 6):
					ih_prob = (math.pow(1 - outcrossing_rate, ih)) * outcrossing_rate
					self.ih_prob_list.append(ih_prob)
				else:
					ih_prob = 1 - sum(self.ih_prob_list)
					self.ih_prob_list.append(ih_prob)