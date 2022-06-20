import sys

from borice.application import *

def main():
	app = Application()
	dataFileName = sys.argv[1]
	#locus_model = [bool(int(sys.argv[2])), bool(int(sys.argv[3])), bool(int(sys.argv[4])), bool(int(sys.argv[5])), bool(int(sys.argv[6])), bool(int(sys.argv[7])), bool(int(sys.argv[8])), bool(int(sys.argv[9])), bool(int(sys.argv[10])), bool(int(sys.argv[11]))]
	locus_model = [bool(int(sys.argv[2])), bool(int(sys.argv[3])), bool(int(sys.argv[4]))]
	numSteps = int(sys.argv[5])
	numBurnInSteps = int(sys.argv[6])
	outcrossingRateTuningParam = float(sys.argv[7])
	alleleFreqTuningParam = float(sys.argv[8])
	outcrossingRate = float(sys.argv[9])
	writeOutput2, writeOutput3, writeOutput4 = True, True, True
	try:
		writeOutput2 = bool(int(sys.argv[10]))
		writeOutput3 = bool(int(sys.argv[11]))
		writeOutput4 = bool(int(sys.argv[12]))
	except:
		pass
	sys.stderr.write(repr(dataFileName) + '\n	 ')
	sys.stderr.write(repr(locus_model) + '\n	 ')
	sys.stderr.write(repr(numSteps) + '\n	 ')
	sys.stderr.write(repr(numBurnInSteps) + '\n   ')
	sys.stderr.write(repr(outcrossingRateTuningParam) + '\n   ')
	sys.stderr.write(repr(alleleFreqTuningParam) + '\n	  ')
	sys.stderr.write(repr(outcrossingRate) + '\n	')
	sys.stderr.write(repr(writeOutput2) + '\n	 ')
	sys.stderr.write(repr(writeOutput3) + '\n	 ')
	sys.stderr.write(repr(writeOutput4) + '\n	 ')
		
	app.run(dataFileName, locus_model, numSteps, numBurnInSteps, outcrossingRateTuningParam, alleleFreqTuningParam, outcrossingRate, writeOutput2, writeOutput3, writeOutput4)

if __name__ == '__main__':
	main()
