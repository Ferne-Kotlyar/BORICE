import argparse

from borice.application import *

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument(dest='datafile',
						help='input data file (formatted as CSV)')

	parser.add_argument('--locus',
						type=bool,
						default=Application.LOCUS_MODEL,
						nargs='*',
						dest='locus_model',
						help='considers null alleles at a given locus if set to True (ex: 0 1 0)')

	parser.add_argument('--steps',
						type=int,
						default=Application.NUM_STEPS,
						dest='steps',
						help='number of steps taken in the MCMC chain. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the chain length is too short.')

	parser.add_argument('--burnin-steps',
						type=int,
						default=Application.BURN_IN,
						dest='burnin_steps',
						help='number of initial steps that will be discarded before the posterior distributions are calculated. If replicate runs of BORICE yield varying estimates of t or F, this may indicate that the burn-in length is too short.')

	parser.add_argument('--outcrossing-tuning',
						type=float,
						default=Application.OUTCROSSING_RATE_TUNING,
						dest='outcrossing_tuning',
						help='determines how large a change in outcrossing rate is made at each step.')

	parser.add_argument('--allele-frequency-tuning',
						type=float,
						default=Application.ALLELE_FREQUENCY_TUNING,
						dest='allele_frequency_tuning',
						help='determines how large a change in allele frequency is made at each step.')

	parser.add_argument('--outcrossing-rate',
						type=float,
						default=Application.INITIAL_OUTCROSSING_RATE,
						dest='outcrossing_rate',
						help='determines the starting outcrossing rate value for the chain.')

	parser.add_argument('--ignore-genotyping-errors',
						action='store_true',
						dest='ignore_genotyping_errors',
						help='skips any offspring that has an allele that does not match the mother if set to True.')

	parser.add_argument('--skip-output-2',
						action='store_false',
						dest='write_output_2',
						help='skips writing the output file 2 (posterior distributions of maternal inbreeding histories).')

	parser.add_argument('--skip-output-3',
						action='store_false',
						dest='write_output_3',
						help='skips writing the output file 3 (list of t and F values from every 10 steps in the MCMC chain).')

	parser.add_argument('--skip-output-4',
						action='store_false',
						dest='write_output_4',
						help='skips writing the output file 4 (posterior distributions for each maternal genotype at each locus in each family).')

	parser.add_argument('--seed',
						type=int,
						default=Application.SEED,
						dest='seed',
						help='custom seed used for random number generation')

	args = parser.parse_args()

	app = Application()

	app.run(args.datafile,
			args.locus_model,
			args.steps,
			args.burnin_steps,
			args.outcrossing_tuning,
			args.allele_frequency_tuning,
			args.outcrossing_rate,
			args.write_output_2,
			args.write_output_3,
			args.write_output_4,
			args.ignore_genotyping_errors,
			args.seed)

if __name__ == '__main__':
	main()
