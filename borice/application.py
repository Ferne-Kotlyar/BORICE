import sys
import os
import math
import random
import time
from decimal import *

from .allele import *
from .csv_utils import *
from .population import *
from .family import *
from .individual import *
from .genotype import *

class Application(object):	
	"""The application class encompasses the main functional components of the BORICE software.
	"""
	# Default Settings
	LOCUS_MODEL = [0, 0, 0]
	NUM_STEPS = 100000
	BURN_IN = 9999
	OUTCROSSING_RATE_TUNING = 0.05
	ALLELE_FREQUENCY_TUNING = 0.1
	INITIAL_OUTCROSSING_RATE = 0.5
	WRITE_OUTPUT_2 = True
	WRITE_OUTPUT_3 = True
	WRITE_OUTPUT_4 = True
	IGNORE_GENOTYPING_ERRORS = False
	SEED = None

	def __init__(self):
		#Progress of calculation
		self.current_step = 0	

	def getStep(self):
		return self.current_step

	def run(self,
			file_name,
			locus_model = LOCUS_MODEL,
			num_steps = NUM_STEPS,
			burn_in = BURN_IN,
			outcrossing_rate_tuning_parameter = OUTCROSSING_RATE_TUNING,
			allele_freq_tuning_parameter = ALLELE_FREQUENCY_TUNING,
			initial_outcrossing_rate = INITIAL_OUTCROSSING_RATE,
			writeOutput2 = WRITE_OUTPUT_2,
			writeOutput3 = WRITE_OUTPUT_3,
			writeOutput4 = WRITE_OUTPUT_4,
			ignore_genotyping_errors = IGNORE_GENOTYPING_ERRORS,
			seed = SEED):

		print('')
		print("Running BORICE with the following settings:")
		print('- Data file: ' + file_name)
		print('- Locus Model: ' + str(locus_model))
		print('- Number of Steps: ' + str(num_steps))
		print('- Burn-in Steps: ' + str(burn_in))
		print('- Outcrossing Tuning Parameter: ' + str(outcrossing_rate_tuning_parameter))
		print('- Allele Frequency Tuning Parameter: ' + str(allele_freq_tuning_parameter))
		print('- Initial Outcrossing Rate: ' + str(initial_outcrossing_rate))
		print('- Ignore Genotyping Errors: ' + str(ignore_genotyping_errors))
		print('- Write Output 2: ' + str(writeOutput2))
		print('- Write Output 3: ' + str(writeOutput3))
		print('- Write Output 4: ' + str(writeOutput4))
		print('- Seed: ' + str(seed))
		print('')

		self.current_step = 0

		# If a custom seed has been provided, initialize the random number generator with this seed.
		if seed:
			random.seed(seed)
		else:
			environmentSeed = os.environ.get('BORICE_RAND_SEED')
			# If no custom seed has been provided and an environment seed exists, initialize the random number generator with this seed.
			if environmentSeed:
				random.seed(int(environmentSeed))

		input = open(file_name, 'r')

		try:
			marker_names, families = parse_csv(input, ',')	
		except CSVFileParseException as x:
			sys.exit(str(x))
		
		assert len(marker_names) == len(locus_model)
		# main body of code begins here
		sorted_alleles_all_loci = []
		allele_freq_all_loci = []
		initial_y_values_all_loci = []
		index = 0
		for marker in marker_names:
			null = locus_model[index]
			# alleles at each locus are identified and missing values eliminated
			num_alleles = marker[1]
			unique_alleles = set(num_alleles)
			unique_alleles.discard(-9)
			#unique_alleles.discard(0)
			# allele list is created and sorted
			sorted_alleles = [0] # need to start the list with zero here; 0 is the null allele (not observed)
			al = list(sorted(unique_alleles))
			sorted_alleles.extend(al)
			sorted_alleles_all_loci.append(sorted_alleles)
			# initial allele frequencies are set
			if null:
				alleles = len(sorted_alleles)
				freq = 1.0 / alleles
				assert freq
				af = [] # the initial allele frequency list; allele zero is the null allele
			else:
				alleles = len(unique_alleles)
				freq = 1.0 / alleles
				assert freq
				af = [0.0] # if no null allele, then allele zero has a frequency of zero
			for i in range(alleles):
				af.append(freq)
			assert af
			allele_freq_all_loci.append(af)
			# makes a list of initial y values; initial y is 1.0 for each allele
			y_values = []
			initial_y_values_all_loci.append(y_values)
			index = index + 1
		assert len(sorted_alleles_all_loci) == len(allele_freq_all_loci) == len(initial_y_values_all_loci)
		population = Population(sorted_alleles_all_loci, allele_freq_all_loci, initial_y_values_all_loci, initial_outcrossing_rate)
		
		#print(population.allele_list)
		#print(population.allele_freq_list)
		#print(population.y_values)
		
		all_alleles = []
		for n, locus in enumerate(population.allele_list):
			alleles = population.allele_list[n]
			locus_alleles = []
			for i, allele in enumerate(alleles):
				allele_object = Allele(allele, locus)
				locus_alleles.append(allele_object)
			all_alleles.append(locus_alleles)

		families = sorted(families)
		# calls the function to initially impute maternal genotypes; also lists families in a population
		for fam in families:
			fam.infer_mom(locus_model, ignore_genotyping_errors) #this gives the initial inference of missing maternal loci; tags loci as imputed
			fam.population_name = population
			population.family_list.append(fam)
			#print(fam)
			#mom_lnL = fam.calc_mom_lnL()
			#print("Log-likelihood of mom = %s" % mom_lnL)
			#progeny_lnL = fam.calc_progeny_lnL(population.outcrossing_rate, locus_model)
			#print("Log-likelihood of progeny = %s" % progeny_lnL)
			#print("Family = %s mom likelihood = %s progeny likelihood = %s" % (fam.name, mom_lnL, progeny_lnL))
			# the below function is called here to catch errors in the progeny genotypes prior to imputing parameters
			#for child in fam.offspring:
			#	child.calc_prob_offspring_geno(fam.population_name.outcrossing_rate, fam.population_name, fam.mom, is_stepping)
		
		#print(population.allele_freq_list)
		#prev_lnL = population.calc_pop_lnL(locus_model)
		#print("Log-likelihood of data = %s" % prev_lnL)
		
		# creates a list of lists for each family for storage of imputed genotypes at each locus
		for fam in families:
			for n, locus in enumerate(fam.mom.genotype_list):
				fam.locus_genotypes.append([])
				fam.possible_genotypes.append([])

		#creates four output files
		borice_output1 = open('BORICE_output1.txt', 'w')
		if(writeOutput2):
			borice_output2 = open('BORICE_output2.txt', 'w')
		if(writeOutput3):
			borice_output3 = open('BORICE_output3.txt', 'w')
			borice_output3.write("List of t, F, and ln likelihoood values from every 10 steps in the chain beyond the burn-in\nt\tF\tLn Likelihood of the Data\n")
		if(writeOutput4):
			borice_output4 = open('BORICE_output4.txt', 'w')
	
		# below lists needed for storage of t, ih, and F before output to text files
		t_list = []
		ih_list = []
		F_list = []
		pop_lnL_list = []
		
		print("start time was %s" % time.asctime())
		start_time = time.time()
		
		# below is the code to perform Bayesian inference of outcrossing rate (t), inbreeding history, allele frequencies, maternal genotypes
		for step in range(num_steps):
			if step != 0:
				self.current_step = step - 1
			
			prev_t = population.outcrossing_rate
			prev_lnL = population.calc_pop_lnL(locus_model)
			#print(prev_lnL)
			# changes outcrossing rate
			t_prime = (prev_t + ((random.random() - 0.5) * float(outcrossing_rate_tuning_parameter)))
			if t_prime < 0.0:
				t_prime = (0.0 - t_prime)
			if t_prime > 1.0:
				t_prime = (2.0 - t_prime)
			population.outcrossing_rate = t_prime
			#print(population.outcrossing_rate)
			lnL = population.calc_pop_lnL(locus_model)
			#print(lnL)
			if (lnL == float('-inf')):
				population.outcrossing_rate = prev_t
				prev_lnL = prev_lnL
				#print("1")
			else:
				lnL_ratio = (lnL - prev_lnL)
				if (lnL_ratio > 0):
					prev_t = population.outcrossing_rate
					prev_lnL = lnL
					#print("2")
				else:
					random_number = random.random()
					value = math.exp(lnL_ratio)
					if (random_number < value):
						prev_t = population.outcrossing_rate
						prev_lnL = lnL
						#print("2")
					else:
						population.outcrossing_rate = prev_t
						prev_lnL = prev_lnL
						#print("1")
	
			if step > burn_in:
				if (step % 10) == 0:
					t_list.append(population.outcrossing_rate)
					if(writeOutput3):
						borice_output3.write("%.2f" % population.outcrossing_rate + "\t")
			
			# changes inbreeding history
			population.calc_ih_prob()
			f_list = []
			for fam in families:
				#print(fam)
				prev_ih = fam.inbreeding_history
				#print(prev_ih)
				prev_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
				#print(prev_f)
				prev_mom_lnL = fam.mom.calc_prob_mom_geno(fam.population_name)
 				#print(prev_mom_lnL)
 				
				rand_num = random.random()
				cumulative_prob = 0
				ih_value = 0
				i = 0
				# choose new inbreeding history value
				while i == 0:
					cumulative_prob = cumulative_prob + population.ih_prob_list[ih_value]
					if rand_num < cumulative_prob:
						new_ih = ih_value
						i = 1
					else:
						ih_value = ih_value + 1
 		
				fam.inbreeding_history = new_ih
				#print(fam.inbreeding_history)
				new_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
				#print(new_f)
				lnL = fam.mom.calc_prob_mom_geno(fam.population_name)
				#print(lnL)
				if (lnL == float('-inf')):
					fam.inbreeding_history = prev_ih
					prev_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
					f_list.append(prev_f)
					#print("1")
				else:
					lnL_ratio = (lnL - prev_mom_lnL)
					if (lnL_ratio > 0):
						prev_ih = fam.inbreeding_history
						new_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
						f_list.append(new_f)
						#print("2")
					else:
						rand = random.random()
						value = math.exp(lnL_ratio)
						if (rand < value):
							prev_ih = fam.inbreeding_history
							new_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
							f_list.append(new_f)
							#print("2")
						else:
							fam.inbreeding_history = prev_ih
							prev_f = fam.mom.calc_inbreeding_coefficient(fam.inbreeding_history)
							f_list.append(prev_f)
							#print("1")
		
				if step > burn_in:
					if (step % 10) == 0:
						ih_list.append(fam.inbreeding_history)
						fam.inbreeding_history_list.append(fam.inbreeding_history)
 			
			pop_inbreeding_coefficient = sum(f_list)/len(f_list)

			if step > burn_in:
				if (step % 10) == 0:
					F_list.append(pop_inbreeding_coefficient)
					if(writeOutput3):
						borice_output3.write("%.2f" % pop_inbreeding_coefficient + "\t")

			del population.ih_prob_list[:]
			
			if (step % 10) == 0:
				# changes allele frequencies
				for locus_index, locus in enumerate(all_alleles):
					allele_freq = population.allele_freq_list[locus_index]
					prev_allele_freq = list(allele_freq)
					#print(prev_allele_freq)
					locus_alleles = all_alleles[locus_index]
					null = locus_model[locus_index]
					if null:
						random_allele = random.randint(0, len(locus_alleles) - 1)
						allele = locus_alleles[random_allele]
					elif len(allele_freq) == 1: # this is to account for single-offspring families with missing data at a locus with no null alleles
						continue
					else:
						random_allele = random.randint(1, len(locus_alleles) - 1) # skips allele zero, which should remain at a frequency of zero with no null alleles
						allele = locus_alleles[random_allele]
						#print(allele)
						
					prev_y = allele.y
					#print(prev_y)
					prev_lnL = population.calc_pop_lnL(locus_model)
					#print(prev_lnL)
					new_y = (prev_y + ((random.random() - 0.5) * float(allele_freq_tuning_parameter)))
					if new_y < 0:
						new_y = (0.0 - new_y)
					allele.y = new_y
					#print(allele.y)
					new_af_list = population.calculate_new_af_list(locus_alleles, locus_index, step, burn_in, locus_model)
					#print(new_af_list)
					#calculates new lnL based on new allele frequencies
					population.allele_freq_list[locus_index] = new_af_list	
					lnL = population.calc_pop_lnL(locus_model)
					#print(lnL)
					population.y_values[locus_index] = []
				
					# decide to step forward or back based on value
					if (lnL == float('-inf')):
						population.allele_freq_list[locus_index] = prev_allele_freq
						allele.y = prev_y
						prev_lnL = prev_lnL
						#print("1")
					else:
						value = math.exp(lnL - prev_lnL) * math.exp(prev_y - new_y)
						if (value > 1):
							prev_y = allele.y
							prev_lnL = lnL
							#print("2")
						else:
							random_number = random.random()
							if (random_number < value):
								prev_y = allele.y
								prev_lnL = lnL
								#print("2")
							else:
								population.allele_freq_list[locus_index] = prev_allele_freq
								allele.y = prev_y
								prev_lnL = prev_lnL
								#print("1")
			
			#changes the genotype at a random maternal locus
			for fam in families:
				#print(fam)
				# returns a tuple containing three lists; the first is the list of imputed genotypes 
				# the second the alleles, and the third the allele frequencies at those imputed loci
				imputed = fam.mom.get_imputed_loci(fam.population_name)
				imputed_genotypes = imputed[0]
				imputed_alleles = imputed[1]
				imputed_af_list = imputed[2]
				
				# determines if there are imputed genotypes; if so, new genotypes are tried and
				# likelihood values calculated for each family
				if (len(imputed_genotypes) == 0):
					continue # if no imputed genotypes are present, go on to the next family
				else:
					# one locus at a time is changed in each family; locus chosen randomly
					random_locus = random.randint(0, len(imputed_genotypes) - 1)
					genotype = imputed_genotypes[random_locus]
					allele_list = imputed_alleles[random_locus]
					allele_freq = imputed_af_list[random_locus]
		
					prev_first = genotype.first
					#print(prev_first)
					prev_second = genotype.second
					#print(prev_second)
					prev_fam_lnL = fam.calc_progeny_lnL(population.outcrossing_rate, locus_model)
					#print(prev_fam_lnL)
					# returns a tuple with new maternal alleles = (new_first, new_second)
					new_mom = genotype.impute_new_mom(allele_list, allele_freq, fam.mom.inbreeding_coefficient, random_locus, locus_model)
					new_first = new_mom[0]
					new_second = new_mom[1]
		
					# sets new maternal alleles and calculates family lnL
					genotype.first = new_first
					genotype.second = new_second
					#print(genotype.first)
					#print(genotype.second)
					new_fam_lnL = fam.calc_progeny_lnL(population.outcrossing_rate, locus_model)
					#print(new_fam_lnL)
					if (new_fam_lnL == float('-inf')):
						genotype.first = prev_first
						genotype.second = prev_second
						#print("1")
					else:
						fam_lnL_ratio = (new_fam_lnL - prev_fam_lnL)
						if (fam_lnL_ratio > 0):
							prev_first = genotype.first
							prev_second = genotype.second
							#print("2")
						else:
							rand = random.random()
							value = math.exp(fam_lnL_ratio)
							if (rand < value):
								prev_first = genotype.first
								prev_second = genotype.second
								#print("2")
							else:
								genotype.first = prev_first
								genotype.second = prev_second
								#print("1")
								
		
				for n, genotype in enumerate(fam.mom.genotype_list):
					if str(genotype) not in fam.possible_genotypes[n]:
						fam.possible_genotypes[n].append(str(genotype))
		
				if step > burn_in:
					if (step % 10) == 0:
						for n, genotype in enumerate(fam.mom.genotype_list):
							fam.locus_genotypes[n].append(str(fam.mom.genotype_list[n]))

			if step > burn_in:
				if (step % 10) == 0:
					pop_lnL_list.append(population.calc_pop_lnL(locus_model))
					if(writeOutput3):
						borice_output3.write("%.6f" % population.calc_pop_lnL(locus_model) + "\n")

		end_time = time.time()
		print("end time was %s" % time.asctime())
		print("executed in %ss" % str(round(end_time - start_time, 2)))

		# main code dealing with file output begins here
		borice_output1.write("Posterior distribution of population inbreeding history:\n")

		for ih_value in range(0, 7):
			ih_count = ih_list.count(ih_value)
			ih_total = len(ih_list)
			ih_percent = float(ih_count)/ih_total
			borice_output1.write("IH value =\t%s\tProportion =\t%.4f\n" % (ih_value, ih_percent))

		borice_output1.write("\nPosterior distributions of t and F:\n")
		borice_output1.write("\nt and F values range from 0 to 1.\nThe below bins represent a range of values greater than or equal to the number listed, but less than the next value.\nExcept bin 1.00, which represents only instances where the t or F value equaled 1.00.\n\n")

		t_percent_list = []
		F_percent_list = []
		bin = 0.0
		while bin < 1.01:
			t_bin_list = []
			for n, t in enumerate(t_list):
				if (t >= bin) and (t < (bin + 0.01)):
					t_bin_list.append(t)
				else:
					continue
			t_count = len(t_bin_list)
			t_percent = float(t_count)/len(t_list)
			t_percent_list.append(t_percent)
			F_bin_list = []
			for n, F in enumerate(F_list):
				if (F >= bin) and (F < (bin + 0.01)):
					F_bin_list.append(F)
				else:
					continue
			F_count = len(F_bin_list)
			F_percent = float(F_count)/len(F_list)
			F_percent_list.append(F_percent)
			borice_output1.write("bin =\t%.2f\tt proportion =\t%.4f\tF proportion =\t%.4f\n" % (bin, t_percent, F_percent))
			bin = bin + 0.01

		t_percent_max = 0.0
		for n, percent in enumerate(t_percent_list):
			if percent > t_percent_max:
				t_percent_max = percent
				t_max = n * 0.01
			else:
				continue
		
		t_list.sort()
		t_lower = int(len(t_list) * 0.025)
		t_lower_percentile = t_list[t_lower]
		t_upper = int(len(t_list) * 0.975)
		t_upper_percentile = t_list[t_upper]
		sum_t = math.fsum(t_list)
		total_t = len(t_list)
		mean_t = (sum_t/total_t)
		borice_output1.write("\nMean t = %.2f; t-max = %.2f; 2.5 percentile = %.2f; 97.5 percentile = %.2f\n" % (mean_t, t_max, t_lower_percentile, t_upper_percentile))

		F_percent_max = 0.0
		for n, percent in enumerate(F_percent_list):
			if percent > F_percent_max:
				F_percent_max = percent
				F_max = n * 0.01
			else:
				continue

		F_list.sort()
		F_lower = int(len(F_list) * 0.025)
		F_lower_percentile = F_list[F_lower]
		F_upper = int(len(F_list) * 0.975)
		F_upper_percentile = F_list[F_upper]
		sum_F = math.fsum(F_list)
		total_F = len(F_list)
		mean_F = (sum_F/total_F)
		borice_output1.write("Mean F = %.2f; F-max = %.2f; 2.5 percentile = %.2f; 97.5 percentile = %.2f\n\n" % (mean_F, F_max, F_lower_percentile, F_upper_percentile))
		
		new_likelihoods = []
		sum_ln_likelihoods = math.fsum(pop_lnL_list)
		total_n = len(pop_lnL_list)
		arithmetic_mean = (sum_ln_likelihoods/total_n)
		borice_output1.write("Ave LL = %s\n" % arithmetic_mean)
# 		for n, ln_likelihood in enumerate(pop_lnL_list):
# 			new_likelihood = Decimal(-(ln_likelihood)).exp()
# 			new_likelihoods.append(new_likelihood)
# 		new_sum = sum(new_likelihoods)
# 		reciprocal_n = math.pow(total_n, -1)
# 		new_reciprocal_n = Decimal(reciprocal_n)
# 		reciprocal_harmonic = new_sum * new_reciprocal_n
# 		harmonic_mean = Decimal(1/reciprocal_harmonic)
# 		borice_output1.write("Harmonic mean of likelihood values = %s\n" % harmonic_mean)
		
		if(writeOutput2):
			borice_output2.write("\nPosterior distributions of maternal inbreeding histories:\n")

		families = sorted(families)
		for fam in families:
			if(writeOutput2):
				borice_output2.write("Maternal Individual %s:\n" % fam.name)
			for ih_value in range(0, 7):
				ih_count = fam.inbreeding_history_list.count(ih_value)
				ih_total = len(fam.inbreeding_history_list)
				ih_percent = float(ih_count)/ih_total
				if(writeOutput2):
					borice_output2.write("IH value =\t%s\tProportion =\t%.4f\n" % (ih_value, ih_percent))

		borice_output1.write("\nPosterior distributions of allele frequencies at each locus:\n")
		borice_output1.write("\nAllele frequency values range from 0 to 1.\nThe below bins represent a range of values greater than or equal to the number listed, but less than the next value.\nExcept bin 1.00, which represents only instances where the allele frequency equaled 1.00.\n\n")
		borice_output1.write("Allele 0 is the null allele. All other alleles are observed in the dataset.\n\n")

		bin = 0.0
		for locus_index, locus in enumerate(all_alleles):
			locus_alleles = all_alleles[locus_index]
			borice_output1.write("Locus %s\n" % (locus_index + 1))
			for n, allele in enumerate(locus_alleles):
				null = locus_model[locus_index]
				if null:
					borice_output1.write("Allele %s\n" % allele.name)
					af_list = allele.af_list
					while bin < 1.01:
						af_bin_list = []
						for i, af in enumerate(af_list):
							if (af >= bin) and (af < (bin + 0.01)):
								af_bin_list.append(af)
							else:
								continue
						af_count = len(af_bin_list)
						af_percent = float(af_count)/len(af_list)
						borice_output1.write("bin =\t%.2f\taf proportion =\t%.4f\n" % (bin, af_percent))
						bin = bin + 0.01
					bin = 0.0
				else:
					if n == 0: # skips allele zero, which is a dummy allele that remains at a frequency of zero
						continue
					else:
						borice_output1.write("Allele %s\n" % allele.name)
						af_list = allele.af_list
						while bin < 1.01:
							af_bin_list = []
							for i, af in enumerate(af_list):
								if (af >= bin) and (af < (bin + 0.01)):
									af_bin_list.append(af)
								else:
									continue
							af_count = len(af_bin_list)
							af_percent = float(af_count)/len(af_list)
							borice_output1.write("bin =\t%.2f\taf proportion =\t%.4f\n" % (bin, af_percent))
							bin = bin + 0.01
						bin = 0.0

		if(writeOutput4):
			borice_output4.write("Posterior distributions for each maternal genotype at each locus in each family.\n")

		for fam in families:
			if(writeOutput4):
				borice_output4.write("Maternal Individual %s:\n" % fam.name)
			for n, locus in enumerate(fam.possible_genotypes):
				if(writeOutput4):
					borice_output4.write("Locus %s\n" % (n + 1))
				possible_genotype_list = fam.possible_genotypes[n]
				locus_list = fam.locus_genotypes[n]
				for i, genotype in enumerate(possible_genotype_list):
					genotype_count = locus_list.count(str(genotype))
					genotype_percent = float(genotype_count)/len(locus_list)
					if(writeOutput4):
						borice_output4.write("possible genotype = \t%s\tproportion =\t%.2f\n" % (genotype, genotype_percent))
		
		#Progress complete
		self.current_step += 1
		
		borice_output1.close()
		if(writeOutput2):
			borice_output2.close()
		if(writeOutput3):
			borice_output3.close()
		if(writeOutput4):
			borice_output4.close()

