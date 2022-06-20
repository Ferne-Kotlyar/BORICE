import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from borice.csv_utils import *
from borice_gui.borice_thread import *

class MainWindow(QMainWindow):
	"""
	This class defines the graphical user interface for the BORICE program,
	allowing for easy user input and data display.
	"""
	def __init__(self,parent,app):

		#initialize superclass and references to the application and parent
		super(MainWindow, self).__init__(parent)
		self.parent = parent
		self.app = app

		#set window size to default and set the icon and window title
		self.resize(700,550)
		self.setWindowTitle("BORICE")
		self.setWindowIcon(QIcon(os.path.join('Images','dna.png')))

		#
		# Input/Output Data
		#
		#Outcrossing Rate. Can range from 0-1
		self.outcrossingRate = 0.50
		#Number of steps
		self.numSteps = 100000
		#Number of steps to burn in
		self.numBurnInSteps = 9999
		#Number of steps taken
		self.numStepsTaken = None
		#Number of marker loci
		self.numMarkerLoci = None
		#Marker loci names
		self.markerLociNames = []
		#Are there population names?
		self.popNamesExist = None
		#Are there subgroup names?
		self.subNamesExist = None

		self.dataFileName = ""

		self.outcrossingRateTuningParam = 0.05
		self.alleleFreqTuningParam = 0.1
		
		self.writeOutput2 = True
		self.writeOutput3 = True
		self.writeOutput4 = True

		self.ignoreGenotypingErrors = False

		#build the user interface
		self.setupUI()

	def setupUI(self):
		"""
		Creates the layout and all widgets for the MainWindow.
		"""
		#Central Widget
		centralWidget = QWidget(self)
		self.setCentralWidget(centralWidget)

		#Central Layout
		centralLayout = QVBoxLayout()
		centralLayout.setAlignment(QtCore.Qt.AlignCenter)
		centralWidget.setLayout(centralLayout)

		#Actions for the Menu Bar
		#Open Data File
		fileOpenAction = QAction("&Open Data File", self)
		fileOpenAction.setShortcut(QKeySequence.Open)
		helpText = "Open a data file"
		fileOpenAction.setToolTip(helpText)
		fileOpenAction.setStatusTip(helpText)
		fileOpenAction.triggered.connect(self.fileOpen)
		#Quit
		fileQuitAction = QAction("&Quit", self)
		fileQuitAction.setShortcut(QKeySequence.Quit)
		helpText = "Exit"
		fileQuitAction.setToolTip(helpText)
		fileQuitAction.setStatusTip(helpText)
		fileQuitAction.triggered.connect(self.close)

		#Menu Bar
		self.fileMenu = self.menuBar().addMenu("&File")
		self.helpMenu = self.menuBar().addMenu("&Help")

		#Add actions to Menu Bar
		self.fileMenu.addAction(fileOpenAction)
		self.fileMenu.addAction(fileQuitAction)
		#self.helpMenu.addAction()
		
		maxStep = 999999999
		posValidator = QIntValidator(0, maxStep, self)
		zeroOneValidator = QDoubleValidator(0, 1, 2, self)
		
		#Max Widths
		maxLineWidth = 250
		
		self.numStepsText = QLineEdit("100000")
		self.numStepsText.textChanged.connect(self.setNumSteps)
		self.numStepsText.setMaximumWidth(maxLineWidth)
		self.numStepsText.setAlignment(QtCore.Qt.AlignRight)
		self.numStepsText.setValidator(posValidator)
		#Number of steps to Burn In input
		self.numStepsBurnInText = QLineEdit("9999")
		self.numStepsBurnInText.textChanged.connect(self.setBurnInSteps)
		self.numStepsBurnInText.setMaximumWidth(maxLineWidth)
		self.numStepsBurnInText.setAlignment(QtCore.Qt.AlignRight)
		self.numStepsBurnInText.setValidator(posValidator)
		#Outcrossing Rate Tuning Parameter
		self.outcrossingRateTuningParamText = QLineEdit("0.05")
		self.outcrossingRateTuningParamText.textChanged.connect(self.setOutcrossingRateTuningParam)
		self.outcrossingRateTuningParamText.setMaximumWidth(maxLineWidth)
		self.outcrossingRateTuningParamText.setAlignment(QtCore.Qt.AlignRight)
		self.outcrossingRateTuningParamText.setValidator(zeroOneValidator)
		#Initial Population Outcrossing Rate
		self.initialPopulationOutcrossingRateText = QLineEdit("0.5")
		self.initialPopulationOutcrossingRateText.textChanged.connect(self.setInitialPopulationOutcrossingRate)
		self.initialPopulationOutcrossingRateText.setValidator(zeroOneValidator)
		self.initialPopulationOutcrossingRateText.setMaximumWidth(maxLineWidth)
		self.initialPopulationOutcrossingRateText.setAlignment(QtCore.Qt.AlignRight)
		#Allele Frequency Tuning Parameter
		self.AlleleFreqTuningParamText = QLineEdit("0.1")
		self.AlleleFreqTuningParamText.textChanged.connect(self.setAlleleFreqTuningParam)
		self.AlleleFreqTuningParamText.setMaximumWidth(maxLineWidth)
		self.AlleleFreqTuningParamText.setAlignment(QtCore.Qt.AlignRight)
		self.AlleleFreqTuningParamText.setValidator(zeroOneValidator)
		#Ignore Genotyping Errors
		self.IgnoreGenotypingErrorsCheckbox = QCheckBox()
		self.IgnoreGenotypingErrorsCheckbox.setChecked(self.ignoreGenotypingErrors)
		self.IgnoreGenotypingErrorsCheckbox.setMaximumWidth(maxLineWidth)
		self.IgnoreGenotypingErrorsCheckbox.toggled.connect(self.setIgnoreGenotypingErrors)

		#Run Button
		runBox = QWidget()
		self.runLayout = QVBoxLayout()
		self.runLayout.setAlignment(QtCore.Qt.AlignCenter)
		runBox.setLayout(self.runLayout)
		self.runButton = QPushButton("Run")
		self.runLayout.addWidget(self.runButton)
		
		#Posterior Distributions of Maternal Inbreeding Histories
		self.outputOptionTwoCheckBox = QCheckBox()
		self.outputOptionTwoCheckBox.setChecked(True)
		self.outputOptionTwoCheckBox.toggled.connect(self.setWrite2)
		
		#List of t and F values
		self.outputOptionThreeCheckBox = QCheckBox()
		self.outputOptionThreeCheckBox.setChecked(True)
		self.outputOptionThreeCheckBox.toggled.connect(self.setWrite3)
		
		#Posterior Distributions for each maternal genotype at each locus in each family
		self.outputOptionFourCheckBox = QCheckBox()
		self.outputOptionFourCheckBox.setChecked(True)
		self.outputOptionFourCheckBox.toggled.connect(self.setWrite4)
		
		#Connect run button to spawn a progress dialog when clicked
		self.runButton.clicked.connect(self.progress)
		
		#Add input widgets to the layout
		settingsBox = QGroupBox("Settings")
		centralLayout.addWidget(settingsBox)
		settingsLayout = QVBoxLayout()
		settingsBox.setLayout(settingsLayout)
		centralLayout.addWidget(runBox)
		
		self.tabWidget = QTabWidget(settingsBox)
		settingsLayout.addWidget(self.tabWidget)
		
		#General settings box (Number of settings known a priori)
		genSettingsBox = QWidget()
		genSettingsLayout = QFormLayout(genSettingsBox)
		genSettingsLayout.setSizeConstraint(QLayout.SetMinimumSize)
		genSettingsLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
		genSettingsLayout.setContentsMargins(0, 0, 0, 0)
		genSettingsLayout.setFormAlignment(QtCore.Qt.AlignCenter)
		genSettingsLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
		genSettingsBox.setLayout(genSettingsLayout)
		genSettingsLayout.addRow("Number of Steps: ", self.numStepsText)
		genSettingsLayout.addRow("Number of Burn In Steps: ", self.numStepsBurnInText)
		genSettingsLayout.addRow("Outcrossing Rate Tuning Parameter: ", self.outcrossingRateTuningParamText)
		genSettingsLayout.addRow("Allele Frequency Tuning Parameter: ", self.AlleleFreqTuningParamText)
		genSettingsLayout.addRow("Initial Population Outcrossing Rate: ", self.initialPopulationOutcrossingRateText)
		genSettingsLayout.addRow("Ignore Genotyping Errors: ", self.IgnoreGenotypingErrorsCheckbox)
		self.tabWidget.addTab(genSettingsBox, "General Settings")
		
		outputOptionsBox = QWidget()
		outputOptionsLayout = QFormLayout(outputOptionsBox)
		outputOptionsLayout.setContentsMargins(0, 0, 0, 0)
		outputOptionsLayout.setFormAlignment(QtCore.Qt.AlignCenter)
		outputOptionsLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
		outputOptionsBox.setLayout(outputOptionsLayout)
		outputOptionsLayout.addRow("Posterior Distributions of Maternal Inbreeding Histories: ", self.outputOptionTwoCheckBox)
		outputOptionsLayout.addRow("List of t and F values", self.outputOptionThreeCheckBox)
		outputOptionsLayout.addRow("Posterior Distributions for each maternal genotype at each locus in each family: ", self.outputOptionFourCheckBox)
		self.tabWidget.addTab(outputOptionsBox, "File Output Options")
		
		infoBox = QWidget()
		infoLayout = QFormLayout()
		infoLayout.setContentsMargins(0, 0, 0, 0)
		infoLayout.setFormAlignment(QtCore.Qt.AlignCenter)
		infoLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
		infoBox.setLayout(infoLayout)
		
		self.numLociLabel = QLabel("")
		self.numLociLabel.setSizePolicy(QSizePolicy.Maximum,
										QSizePolicy.Maximum)
		self.numFamiliesLabel = QLabel("")
		self.numFamiliesLabel.setSizePolicy(QSizePolicy.Maximum,
										QSizePolicy.Maximum)
		self.numIndividualsLabel = QLabel("")
		self.numIndividualsLabel.setSizePolicy(QSizePolicy.Maximum,
										QSizePolicy.Maximum)

		infoLayout.addRow("Number of Marker Loci: ", self.numLociLabel)
		infoLayout.addRow("Number of Families: ", self.numFamiliesLabel)
		infoLayout.addRow("Number of Individuals: ", self.numIndividualsLabel)
		self.tabWidget.addTab(infoBox, "Input Data Summary")


		#Hide the interface until the user opens a file
		self.centralWidget().hide()
	
	def addUI(self):
		"""Adds the Locus Settings Window to the Main Window.
		"""
		#Locus CheckBox
		locusCheckBoxList = []
		for n, locus in enumerate(self.locusModel):
			locusCheckBox = QCheckBox(str(n), self)
			palette = locusCheckBox.palette()
			palette.setColor(QPalette.WindowText, QColor(0,0,0,0))
			locusCheckBox.setPalette(palette)
			locusCheckBox.setChecked(False)
			locusCheckBox.toggled.connect(self.setLocus)
			locusCheckBoxList.append(locusCheckBox)
		self.locusCheckBoxList = locusCheckBoxList

		#Locus settings box (Number of settings determined by input data file)
		locusSettingsBox = QWidget()
		locusSettingsLayout = QFormLayout(locusSettingsBox)
		locusSettingsLayout.setContentsMargins(0, 0, 0, 0)
		locusSettingsLayout.setFormAlignment(QtCore.Qt.AlignCenter)
		locusSettingsLayout.setLabelAlignment(QtCore.Qt.AlignLeft)
		locusSettingsBox.setLayout(locusSettingsLayout)
		for n, locusCheckBox in enumerate(self.locusCheckBoxList):
			locusSettingsLayout.addRow("Locus %s: " % (n + 1), locusCheckBox)
		self.tabWidget.addTab(locusSettingsBox, "Locus Settings")

	def setBurnInSteps(self, steps):
		if steps:			
			self.numBurnInSteps = int(str(steps))

	def setNumSteps(self, steps):
		if steps:
			self.numSteps = int(str(steps))
			
	def setOutcrossingRateTuningParam(self, tuningParam):
		if tuningParam:
			self.outcrossingRateTuningParam = tuningParam
			
	def setAlleleFreqTuningParam(self, tuningParam):
		if tuningParam:
			self.alleleFreqTuningParam = tuningParam

	def setIgnoreGenotypingErrors(self, value):
		self.ignoreGenotypingErrors = value
	
	def setInitialPopulationOutcrossingRate(self, outcrossingRate):
		if outcrossingRate:
			self.outcrossingRate = outcrossingRate
	
	def setLocus(self, null_locus):
		sender = self.sender()
		i = int(sender.text())
		self.locusModel[i] = null_locus
	
	def setWrite2(self, writeOutput2):
		self.writeOutput2 = writeOutput2
	
	def setWrite3(self, writeOutput3):
		self.writeOutput3 = writeOutput3
	
	def setWrite4(self, writeOutput4):
		self.writeOutput4 = writeOutput4
	
	def fileOpen(self):
		self.dataFileName, _ = QFileDialog.getOpenFileName(self, "Open Data File", ".", "Data Files (*.csv)")
		#Populate data entry tables for Allele Frequency Selection and Inbreeding History Selection
		if(self.dataFileName):
			dataFile = open(self.dataFileName, "rU")
			try:
				marker_names, families = parse_csv(dataFile, ',')	
			except CSVFileParseException as x:
				sys.exit(str(x))

			dataFile = open(self.dataFileName, "rU")
			numIndividuals = 0
			for line in dataFile:
				if line.strip():
					numIndividuals += 1

			numIndividuals -= 2
			
			# the default model for each locus is False, meaning null alleles are not considered at that locus
			self.locus_list = marker_names
			locusModelList = []
			for locus in self.locus_list:
				null_locus = False
				locusModelList.append(null_locus)
			self.locusModel = locusModelList
			
			self.numLociLabel.setText(str(len(marker_names)))
			self.numFamiliesLabel.setText(str(len(families)))
			self.numIndividualsLabel.setText(str(numIndividuals))

			self.addUI()
			self.centralWidget().show()
		else:
			pass
				
	def progress(self):
		#Progress Dialog
		if not self.numSteps:
			message = QMessageBox(self)
			message.setWindowTitle("Error")
			message.setText("Please enter a value for the number of steps!")
			message.exec_()
			return

		if not self.numBurnInSteps:
			message = QMessageBox(self)
			message.setWindowTitle("Error")
			message.setText("Please enter a value for the number of burn in steps!")
			message.exec_()
			return

		numSteps = self.numSteps
		self.progress = QProgressDialog("Calculating...", "Stop", 0, numSteps, self)
		self.progress.setWindowModality(QtCore.Qt.WindowModal)
		self.progress.resize(300,125)
		self.progress.setWindowTitle("Calculating...")
		self.progress.show()
		self.runButton.hide()

		thread = BoriceThread(self, self.dataFileName, self.locusModel, self.numSteps, self.numBurnInSteps, self.outcrossingRateTuningParam, self.alleleFreqTuningParam, self.outcrossingRate, self.writeOutput2, self.writeOutput3, self.writeOutput4, self.ignoreGenotypingErrors)

		thread.start()
		canceled = False

		while thread.getStep() != self.numSteps - 1:
			self.progress.setValue(int(100 * thread.getStep()/self.numSteps))
			QApplication.instance().processEvents()			
			if(self.progress.wasCanceled()):
				thread.quit()
				canceled = True				
				break
		self.progress.setValue(self.numSteps)
		self.runButton.show()
	
		if canceled:
			return

		message = QMessageBox(self)
		message.setWindowTitle("Complete!")
		message.setText("Done! Please look in your current working directory for output files.")
		message.exec_()
		return
	