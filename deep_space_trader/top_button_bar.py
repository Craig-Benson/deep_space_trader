from deep_space_trader.store import Store
from deep_space_trader.utils import errorDialog, yesNoDialog, infoDialog

from PyQt5 import QtWidgets, QtCore, QtGui


class ButtonBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ButtonBar, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.storeButton = QtWidgets.QPushButton("Go to store")
        self.storeButton.clicked.connect(self.storeButtonClicked)
        self.mainLayout.addWidget(self.storeButton)

        self.dayButton = QtWidgets.QPushButton("Go to next day")
        self.dayButton.clicked.connect(self.dayButtonClicked)
        self.mainLayout.addWidget(self.dayButton)

    def storeButtonClicked(self):
        dialog = Store(self.parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def dayButtonClicked(self):
        if self.parent.state.next_day():
            # Days remaining
            self.parent.infoBar.update()
            self.parent.planetItemBrowser.update()
        else:
            # No days remaining
            infoDialog(self, "Game complete", message="You are done")

            self.parent.state.initialize()
            self.parent.infoBar.update()
            self.parent.locationBrowser.update()
            self.parent.playerItemBrowser.update()
            self.parent.planetItemBrowser.update()
            self.parent.warehouseItemBrowser.update()

    def useButtonClicked(self):
        dialog = StoreItemSelector(self.parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()
