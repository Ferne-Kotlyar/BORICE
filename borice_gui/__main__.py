import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main_window import *

def main():
	app = QApplication(sys.argv)
	window = MainWindow(None, app)
	window.show()
	sys.exit(app.exec_())

class TestWindow(QMainWindow):
	def __init__(self, parent, app):
		super(TestWindow, self).__init__(parent)
		self.parent = parent
		self.app = app

		self.resize(500,350)
		self.setWindowTitle("BORICE")

		self.buildUI()

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

		tabs = QTabWidget()

		# General Settings Box
		settingsBox = QWidget()
		settingsBoxForm = QFormLayout(settingsBox)
		settingsBoxForm.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
		settingsBoxForm.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
		settingsBox.setLayout(settingsBoxForm)

		tabs.addTab(settingsBox, "Main")

		# Foo
		foo = QCheckBox()
		foo.setChecked(False)
		foo.setMaximumWidth(250)
		settingsBoxForm.addRow("Foo this is the way lol this is very long string!!!!!", foo)

		

		# Populate the central layout
		centralLayout.addWidget(tabs)

if __name__ == '__main__': 
	main()
