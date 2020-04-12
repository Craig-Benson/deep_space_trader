import sys
import os

from deep_space_trader.main_widget import MainWidget

from PyQt5 import QtWidgets, QtGui, QtCore

from deep_space_trader import __maintainer__ as package_author
from deep_space_trader import __email__ as author_email
from deep_space_trader import __name__ as package_name
from deep_space_trader import __version__ as package_version


def textDisplayWindow(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setInformativeText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, primary_screen):
        super(MainWindow, self).__init__()

        self.primary_screen = primary_screen
        self.initUi()

    def initUi(self):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        imageDir = os.path.join(scriptDir, 'images')
        #self.iconPath = os.path.join(imageDir, 'logo.png')
        #self.compassPath = os.path.join(imageDir, 'compass.png')
        #self.setWindowIcon(QtGui.QIcon(self.iconPath))

        self.widget = MainWidget(self.primary_screen, self)
        self.setCentralWidget(self.widget)

        # Build menu bar
        menu = self.menuBar()
        fileMenu = menu.addMenu("File")

        helpMenu = menu.addMenu("Help")

    def closeEvent(self, event):
        if self.widget.warningBeforeQuit():
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(app.primaryScreen())
    win.setWindowTitle("Deep Space Trader %s" % package_version)
    win.show()
    sys.exit(app.exec_())
