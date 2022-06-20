from PyQt5 import QtCore

from borice.application import Application

class BoriceThread(QtCore.QThread):
	def __init__(self, parent, dataFileName, locusModel, numSteps, numBurnInSteps, outcrossingRateTuningParam, alleleFreqTuningParam, outcrossingRate, writeOutput2, writeOutput3, writeOutput4, ignoreGenotypingErrors):
		super(BoriceThread, self).__init__(parent)
		self.dataFileName = dataFileName
		self.locusModel = locusModel
		self.numSteps = numSteps
		self.numBurnInSteps = numBurnInSteps
		self.outcrossingRateTuningParam = outcrossingRateTuningParam
		self.alleleFreqTuningParam = alleleFreqTuningParam
		self.outcrossingRate = outcrossingRate
		self.writeOutput2 = writeOutput2
		self.writeOutput3 = writeOutput3
		self.writeOutput4 = writeOutput4
		self.ignoreGenotypingErrors = ignoreGenotypingErrors
		self.app = Application()

	def run(self):
		self.app.run(self.dataFileName, self.locusModel, self.numSteps, self.numBurnInSteps, self.outcrossingRateTuningParam, self.alleleFreqTuningParam, self.outcrossingRate, self.writeOutput2, self.writeOutput3, self.writeOutput4, self.ignoreGenotypingErrors)

	def getStep(self):
		return self.app.getStep()
        