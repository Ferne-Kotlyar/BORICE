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

if __name__ == '__main__': 
	main()
