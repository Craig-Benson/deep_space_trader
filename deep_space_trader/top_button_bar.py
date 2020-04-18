from deep_space_trader.utils import errorDialog, yesNoDialog, infoDialog

from PyQt5 import QtWidgets, QtCore, QtGui


class StoreItemSelector(QtWidgets.QDialog):
    def __init__(self, parent):
        super(StoreItemSelector, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        buttonLayout = QtWidgets.QHBoxLayout()

        self.selectButton = QtWidgets.QPushButton("Use item")
        self.selectButton.clicked.connect(self.selectButtonClicked)
        buttonLayout.addWidget(self.selectButton)

        self.mainLayout.addLayout(buttonLayout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(['Item'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.table.resizeColumnsToContents()

        self.mainLayout.addWidget(self.table)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Select item to use")

        self.update()

    def selectButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, message="Please select an item to use first")
            return

        item = self.parent.state.store_items[selectedRow]
        item.use(self.parent)
        del self.parent.state.store_items[selectedRow]
        self.close()

    def addRow(self, item):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)

        item1 = QtWidgets.QTableWidgetItem(item.name)
        item1.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.table.setItem(nextFreeRow, 0, item1)

    def populateTable(self):
        self.table.setRowCount(0)
        for item in self.parent.state.store_items:
            self.addRow(item)

    def update(self):
        self.populateTable()
        super(StoreItemSelector, self).update()

    def sizeHint(self):
        return QtCore.QSize(600, 400)



class ButtonBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ButtonBar, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QHBoxLayout(self)

        self.useButton = QtWidgets.QPushButton("Use item from store")
        self.useButton.clicked.connect(self.useButtonClicked)
        self.mainLayout.addWidget(self.useButton)

        self.storeButton = QtWidgets.QPushButton("Go to store")
        self.storeButton.clicked.connect(self.storeButtonClicked)
        self.mainLayout.addWidget(self.storeButton)

        self.dayButton = QtWidgets.QPushButton("Go to next day")
        self.dayButton.clicked.connect(self.dayButtonClicked)
        self.mainLayout.addWidget(self.dayButton)

    def storeButtonClicked(self):
        pass

    def dayButtonClicked(self):
        pass

    def useButtonClicked(self):
        dialog = StoreItemSelector(self.parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()
