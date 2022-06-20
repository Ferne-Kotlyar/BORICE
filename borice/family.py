from .individual import *
from .genotype import *

class Family(object):
	"""A Family object is a maternal individual, its offspring, and its inbreeding history.
	"""
	def __init__(self, name):
		self.name = name
		self.mom = None
		self.pop_name = None
		self.offspring = []
		self.inbreeding_history_list = []
		self.inbreeding_history = 0
		self.locus_genotypes = []
		self.possible_genotypes = []
	
	def add_mom(self, mom):
		"""Adds a mom to a family unless one's already there.
		"""
		assert self.mom is None
		self.mom = mom
				
	def add_offspring(self, offspring):
		"""Adds offspring to a family."""
		self.offspring.append(offspring)
	
	def infer_mom(self, null_loci, ignore_genotyping_errors):
		"""Infers a maternal genotype for a family from offspring data.
		"""
		# constructs a list of observed alleles
		first_child = self.offspring[0]
		num_loci = len(first_child.genotype_list)
		observed_alleles = []
		for i in range(num_loci):
			observed_alleles.append(set())

		# adds observed alleles at each locus 
		for child in self.offspring:
			for i in range(num_loci):
				cg = child.genotype_list[i]
				allele_set = observed_alleles[i]
				allele_set.add(cg.first)
				allele_set.add(cg.second)
				allele_set.discard(-9)
				null = null_loci[i]
				if null:
					allele_set.add(0)

		# case for no mom genotype
		if not self.mom:
			mom_geno_list = []
			for i in range(num_loci):
				allele_set = observed_alleles[i]
				if len(allele_set) == 0:
					mg = None
				else:
					mg = find_mom_genotype(allele_set, self.offspring, i, null_loci, self.name)
					assert mg
				mom_geno_list.append(mg)
			assert len(mom_geno_list) == num_loci
			the_family = self
			self.mom = Individual(the_family, mom_geno_list, is_mom = True)
		# case for partial mom genotype; some loci inferred
		else:
			mgl = self.mom.genotype_list
			missing = []
			for n, geno in enumerate(mgl):
				if (geno.first == -9) and (geno.second == -9):
					missing.append(n)
				else: # case for observed mom, but null allele possible
					mg = tag_mom_genotype(geno.first, geno.second, self.offspring, n, null_loci, self.name, ignore_genotyping_errors)
					assert mg
					self.mom.genotype_list[n] = mg
					
			for i in missing: # this section imputes a possible genotype for the missing loci
				allele_set = observed_alleles[i]
				if len(allele_set) == 0:
					mg = None
				else:
					mg = find_mom_genotype(allele_set, self.offspring, i, null_loci, self.name)
					assert mg
				self.mom.genotype_list[i] = mg

	def __lt__(self, other):
		return str(self) < str(other)
				
	def __str__(self):
		"""Returns a string identifying a family and its maternal individual.
		"""
		r = ["\nFamily = %s \nMaternal %s" % (self.name, self.mom)]
		for o in self.offspring:
			r.append(str(o))
		return "\nProgeny ".join(r)

	def calc_mom_lnL(self):
		"""Calculates the ln likelihood value for the mom of a family.
		"""
		lnL = self.mom.calc_prob_mom_geno(self.population_name)
		return lnL
		
	def calc_family_lnL(self, outcrossing_rate, null_loci):
		"""Calculates the ln likelihood value for the entire family (mom and offspring).
		"""
		lnL = 0.0
		for offspring in self.offspring:
			lnL = lnL + offspring.calc_prob_offspring_geno(outcrossing_rate, self.population_name, self.mom, null_loci)
		lnL = lnL + self.mom.calc_prob_mom_geno(self.population_name)
		return lnL
	
	def calc_progeny_lnL(self, outcrossing_rate, null_loci):
		"""Calculates the ln likelihood value for only the offspring of a family.
		"""
		lnL = 0.0
		for offspring in self.offspring:
			lnL = lnL + offspring.calc_prob_offspring_geno(outcrossing_rate, self.population_name, self.mom, null_loci)
		return lnL