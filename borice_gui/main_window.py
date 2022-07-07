import sys
import os
import webbrowser

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
	# Constants
	INPUT_FIELD_MINIMUM_WIDTH = 150
	MAX_INT = 999999999

	def __init__(self,parent,app):
		# Initialize superclass and references to the application and parent
		super(MainWindow, self).__init__(parent)
		self.parent = parent
		self.app = app

		# Set window size to default and set the icon and window title
		self.resize(500,350)
		self.setWindowTitle("BORICE")

		# Settings
		self.dataFileName = None
		self.outcrossingRate = Application.INITIAL_OUTCROSSING_RATE
		self.numSteps = Application.NUM_STEPS
		self.numBurnInSteps = Application.BURN_IN
		self.outcrossingRateTuningParam = Application.OUTCROSSING_RATE_TUNING
		self.alleleFreqTuningParam = Application.ALLELE_FREQUENCY_TUNING
		self.ignoreGenotypingErrors = Application.IGNORE_GENOTYPING_ERRORS
		self.writeOutput2 = Application.WRITE_OUTPUT_2
		self.writeOutput3 = Application.WRITE_OUTPUT_3
		self.writeOutput4 = Application.WRITE_OUTPUT_4

		# Build the user interface
		self.buildUI()

	def resetSettings(self):
		"""
		Resets settings to their default values
		"""
		# General Settings
		self.numStepsText.setValue(Application.NUM_STEPS)
		self.numStepsBurnInText.setValue(Application.BURN_IN)
		self.initialPopulationOutcrossingRateText.setValue(Application.INITIAL_OUTCROSSING_RATE)
		self.outcrossingRateTuningParamText.setValue(Application.OUTCROSSING_RATE_TUNING)
		self.AlleleFreqTuningParamText.setValue(Application.ALLELE_FREQUENCY_TUNING)
		self.ignoreGenotypingErrorsCheckbox.setChecked(Application.IGNORE_GENOTYPING_ERRORS)

		# File Output Settings
		self.writeOutput2Checkbox.setChecked(Application.WRITE_OUTPUT_2)
		self.writeOutput3Checkbox.setChecked(Application.WRITE_OUTPUT_3)
		self.writeOutput4Checkbox.setChecked(Application.WRITE_OUTPUT_4)

		# Locus Settings
		for checkbox in self.locusCheckBoxList:
			checkbox.setChecked(False)

	def buildUI(self):
		"""
		Creates the layout and all widgets for the MainWindow.
		"""
		# Central Widget
		centralWidget = QWidget(self)
		centralLayout = QVBoxLayout()
		centralLayout.setAlignment(QtCore.Qt.AlignCenter)
		centralWidget.setLayout(centralLayout)
		self.setCentralWidget(centralWidget)

		# Populate the Menu Bar
		self.populateMenuBar()
		
		# Create Tabs
		self.tabs = QTabWidget()
		self.startupPage = self.createStartupTab()
		self.startupPageTabIndex = self.tabs.addTab(self.startupPage, "Get Started")

		# Create Action Box
		self.actionBox = self.createActionBox()

		# Populate the central layout
		centralLayout.addWidget(self.tabs)
		centralLayout.addWidget(self.actionBox)
		
		# Disable the interface until the user opens a file
		self.actionBox.setDisabled(True)

	def populateMenuBar(self):
		"""
		Populate the menu bar
		"""
		# Open Data File
		fileOpenAction = QAction("&Open Data File", self)
		fileOpenAction.setShortcut(QKeySequence.StandardKey.Open)
		helpText = "Open a data file"
		fileOpenAction.setToolTip(helpText)
		fileOpenAction.setStatusTip(helpText)
		fileOpenAction.triggered.connect(self.openFile)

		# Quit
		fileQuitAction = QAction("&Quit", self)
		fileQuitAction.setShortcut(QKeySequence.StandardKey.Quit)
		helpText = "Exit"
		fileQuitAction.setToolTip(helpText)
		fileQuitAction.setStatusTip(helpText)
		fileQuitAction.triggered.connect(self.close)

		# About
		aboutAction = QAction("&About", self)
		helpText = "About"
		aboutAction.setToolTip(helpText)
		aboutAction.triggered.connect(self.about)

		# Populate menu bar
		fileMenu = self.menuBar().addMenu("&File")
		helpMenu = self.menuBar().addMenu("&Help")

		# Populate file menu
		fileMenu.addAction(fileOpenAction)
		fileMenu.addAction(fileQuitAction)
		helpMenu.addAction(aboutAction)

	def updateFormLayoutStyle(self, formLayout: QFormLayout):
		"""
		Update the form layout style to keep a consistent style across the tabs
		"""
		formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
		formLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

	def createStartupTab(self):
		"""
		Create the startup box
		"""
		# Create Startup Tab
		startupBox = QWidget()
		startupBoxLayout = QVBoxLayout()
		startupBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		startupBox.setLayout(startupBoxLayout)

		# Welcome Message
		welcomeMessage = QLabel("Welcome to BORICE!\nPlease select the data file you want to work with.")
		welcomeMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
		startupBoxLayout.addWidget(welcomeMessage)

		# Open File Button
		selectFileButton = QPushButton("Open Data File")
		selectFileButton.clicked.connect(self.openFile)
		startupBoxLayout.addWidget(selectFileButton)

		return startupBox

	def createNumberWidget(self, type, value, min, max, step, onChanged):
		widget = type()
		widget.setRange(min, max)
		widget.setValue(value)
		widget.valueChanged.connect(onChanged)
		widget.setSingleStep(step)
		return widget

	def createGeneralSettingsTab(self):
		"""
		Creates the general settings tab
		"""
		# General Settings Box
		genSettingsBox = QWidget()
		genSettingsLayout = QFormLayout(genSettingsBox)
		self.updateFormLayoutStyle(genSettingsLayout)
		genSettingsBox.setLayout(genSettingsLayout)

		# Number of steps
		self.numStepsText = self.createNumberWidget(QSpinBox, self.numSteps, 0, self.MAX_INT, 1, self.setNumSteps)
		self.numStepsText.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Number of Steps:", self.numStepsText)

		# Number of steps to Burn In input
		self.numStepsBurnInText = self.createNumberWidget(QSpinBox, self.numBurnInSteps, 0, self.MAX_INT, 1, self.setBurnInSteps)
		self.numStepsBurnInText.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Number of Burn In Steps:", self.numStepsBurnInText)

		# Initial Population Outcrossing Rate
		self.initialPopulationOutcrossingRateText = self.createNumberWidget(QDoubleSpinBox, self.outcrossingRate, 0.0, 1.0, 0.05, self.setInitialPopulationOutcrossingRate)
		self.initialPopulationOutcrossingRateText.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Initial Population Outcrossing Rate:", self.initialPopulationOutcrossingRateText)

		# Outcrossing Rate Tuning Parameter
		self.outcrossingRateTuningParamText = self.createNumberWidget(QDoubleSpinBox, self.outcrossingRateTuningParam, 0.0, 1.0, 0.05, self.setOutcrossingRateTuningParam)
		self.outcrossingRateTuningParamText.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Outcrossing Rate Tuning Parameter:", self.outcrossingRateTuningParamText)

		# Allele Frequency Tuning Parameter
		self.AlleleFreqTuningParamText = self.createNumberWidget(QDoubleSpinBox, self.alleleFreqTuningParam, 0.0, 1.0, 0.05, self.setAlleleFreqTuningParam)
		self.AlleleFreqTuningParamText.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Allele Frequency Tuning Parameter:", self.AlleleFreqTuningParamText)

		# Ignore Genotyping Errors
		self.ignoreGenotypingErrorsCheckbox = QCheckBox()
		self.ignoreGenotypingErrorsCheckbox.setChecked(self.ignoreGenotypingErrors)
		self.ignoreGenotypingErrorsCheckbox.toggled.connect(self.setIgnoreGenotypingErrors)
		self.ignoreGenotypingErrorsCheckbox.setMinimumWidth(self.INPUT_FIELD_MINIMUM_WIDTH)
		genSettingsLayout.addRow("Ignore Genotyping Errors:", self.ignoreGenotypingErrorsCheckbox)

		return genSettingsBox

	def createFileOutputSettingsTab(self):
		"""
		Creates the file output settings tab
		"""
		# Create File Output Settings
		outputOptionsBox = QWidget()
		outputOptionsLayout = QFormLayout(outputOptionsBox)
		self.updateFormLayoutStyle(outputOptionsLayout)
		outputOptionsBox.setLayout(outputOptionsLayout)

		# Posterior Distributions of Maternal Inbreeding Histories
		self.writeOutput2Checkbox = QCheckBox()
		self.writeOutput2Checkbox.setChecked(self.writeOutput2)
		self.writeOutput2Checkbox.toggled.connect(self.setWrite2)
		outputOptionsLayout.addRow("Posterior distributions of maternal inbreeding histories:", self.writeOutput2Checkbox)
		
		# List of t and F values
		self.writeOutput3Checkbox = QCheckBox()
		self.writeOutput3Checkbox.setChecked(self.writeOutput3)
		self.writeOutput3Checkbox.toggled.connect(self.setWrite3)
		outputOptionsLayout.addRow("List of t and F values:", self.writeOutput3Checkbox)
		
		# Posterior Distributions for each maternal genotype at each locus in each family
		self.writeOutput4Checkbox = QCheckBox()
		self.writeOutput4Checkbox.setChecked(self.writeOutput4)
		self.writeOutput4Checkbox.toggled.connect(self.setWrite4)
		outputOptionsLayout.addRow("Posterior distributions for each maternal genotype at each locus in each family:", self.writeOutput4Checkbox)

		return outputOptionsBox

	def createInputDataSummaryTab(self, markerLociCount, familyCount, individualCount):
		"""
		Creates the input data summary tab
		"""
		infoBox = QWidget()
		infoLayout = QFormLayout()
		self.updateFormLayoutStyle(infoLayout)
		infoBox.setLayout(infoLayout)

		dataFileNameLabel = QLabel(os.path.basename(self.dataFileName))
		infoLayout.addRow("Data File:", dataFileNameLabel)
		
		numLociLabel = QLabel(str(markerLociCount))
		infoLayout.addRow("Marker Loci:", numLociLabel)

		numFamiliesLabel = QLabel(str(familyCount))
		infoLayout.addRow("Families:", numFamiliesLabel)

		numIndividualsLabel = QLabel(str(individualCount))
		infoLayout.addRow("Individuals:", numIndividualsLabel)

		return infoBox

	def createLocusSettingsTab(self):
		"""
		Creates the locus settings tab
		"""
		#Locus settings box (Number of settings determined by input data file)
		locusSettingsBox = QWidget()
		locusSettingsLayout = QFormLayout(locusSettingsBox)
		self.updateFormLayoutStyle(locusSettingsLayout)
		locusSettingsBox.setLayout(locusSettingsLayout)

		self.locusCheckBoxList = []
		for n, _ in enumerate(self.locusModel):
			locusCheckBox = QCheckBox(str(n), self)
			palette = locusCheckBox.palette()
			palette.setColor(QPalette.WindowText, QColor(0,0,0,0))
			locusCheckBox.setPalette(palette)
			locusCheckBox.setChecked(False)
			locusCheckBox.toggled.connect(self.setLocus)
			self.locusCheckBoxList.append(locusCheckBox)

		for n, locusCheckBox in enumerate(self.locusCheckBoxList):
			locusSettingsLayout.addRow("Locus %s: " % (n + 1), locusCheckBox)

		return locusSettingsBox

	def createActionBox(self):
		"""
		Creates the action box
		"""
		# Create Action Box
		actionBox = QWidget()
		actionBoxLayout = QHBoxLayout()
		actionBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		actionBox.setLayout(actionBoxLayout)

		# Create Run Button
		runButton = QPushButton("Run")
		runButton.clicked.connect(self.run)
		runButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		actionBoxLayout.addWidget(runButton)

		# Create Reset to Default Button
		defaultbutton = QPushButton("Default")
		defaultbutton.clicked.connect(self.resetSettings)
		defaultbutton.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
		actionBoxLayout.addWidget(defaultbutton)

		return actionBox		

	def setBurnInSteps(self, value):
		self.numBurnInSteps = int(str(value))

	def setNumSteps(self, value):
		self.numSteps = int(str(value))
			
	def setOutcrossingRateTuningParam(self, value):
		self.outcrossingRateTuningParam = value
			
	def setAlleleFreqTuningParam(self, value):
		self.alleleFreqTuningParam = value

	def setIgnoreGenotypingErrors(self, value):
		self.ignoreGenotypingErrors = value
	
	def setInitialPopulationOutcrossingRate(self, value):
		self.outcrossingRate = value
	
	def setLocus(self, value):
		sender = self.sender()
		i = int(sender.text())
		self.locusModel[i] = value
	
	def setWrite2(self, value):
		self.writeOutput2 = value
	
	def setWrite3(self, value):
		self.writeOutput3 = value
	
	def setWrite4(self, value):
		self.writeOutput4 = value
	
	def openFile(self):
		self.dataFileName, _ = QFileDialog.getOpenFileName(self, "Open Data File", ".", "Data Files (*.csv)")

		# Populate data entry tables for Allele Frequency Selection and Inbreeding History Selection
		if (self.dataFileName):
			dataFile = open(self.dataFileName, "r")

			try:
				marker_names, families = parse_csv(dataFile, ',')	
			except CSVFileParseException as x:
				sys.exit(str(x))

			numIndividuals = 0

			for line in dataFile:
				if line.strip():
					numIndividuals += 1

			numIndividuals -= 2
			
			# The default model for each locus is False, meaning null alleles are not considered at that locus
			self.locus_list = marker_names
			locusModelList = []
			for _ in self.locus_list:
				null_locus = False
				locusModelList.append(null_locus)
			self.locusModel = locusModelList

			self.tabs.clear()

			# Create Tabs
			self.generalSettings = self.createGeneralSettingsTab()
			self.fileOutputSettings = self.createFileOutputSettingsTab()
			self.locusSettings = self.createLocusSettingsTab()
			self.inputDataSummary = self.createInputDataSummaryTab(len(marker_names), len(families), numIndividuals)

			# Add Tabs
			self.generalSettingsTabIndex = self.tabs.addTab(self.generalSettings, "General Settings")
			self.fileOutputSettingsTabIndex = self.tabs.addTab(self.fileOutputSettings, "File Output Settings")
			self.locusSettingsTabIndex = self.tabs.addTab(self.locusSettings, "Locus Settings")
			self.inputDataSummaryTabIndex = self.tabs.addTab(self.inputDataSummary, "Input Data Summary")

			self.actionBox.setDisabled(False)
		else:
			pass
				
	def about(self):
		"""
		Open BORICE GitHub repository in the default web browser
		"""
		webbrowser.open("https://github.com/Ferne-Kotlyar/BORICE")

	def run(self):
		"""
		Run BORICE with the current settings
		"""
		numSteps = self.numSteps
		progress = QProgressDialog("Processing %s" % os.path.basename(self.dataFileName), "Stop", 0, numSteps, self)
		progress.setWindowModality(Qt.WindowModal)
		progress.resize(300,125)
		progress.setWindowTitle("Calculating...")
		progress.show()

		thread = BoriceThread(self, self.dataFileName, self.locusModel, self.numSteps, self.numBurnInSteps, self.outcrossingRateTuningParam, self.alleleFreqTuningParam, self.outcrossingRate, self.writeOutput2, self.writeOutput3, self.writeOutput4, self.ignoreGenotypingErrors)
		
		thread.start()

		while thread.getStep() != self.numSteps - 1:
			progress.setValue(int(thread.getStep()))
			QApplication.instance().processEvents()			
			if (progress.wasCanceled()):
				thread.terminate()
				return

		progress.setValue(self.numSteps)
	
		message = QMessageBox(self)
		message.setWindowTitle("Success!")
		message.setText("Calculation completed!\nPlease look in your current working directory for output files.")
		message.exec_()
	