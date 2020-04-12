from PyQt5 import QtWidgets, QtCore, QtGui


class PlayerItemBrowser(QtWidgets.QWidget):
    def __init__(self, parent):
        super(PlayerItemBrowser, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        #self.button1 = QtWidgets.QPushButton()
        #self.button1.setText("B1")

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Item type', 'Quantity'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.populateTable()

        self.mainLayout.addWidget(self.table)

    def addRow(self, itemname):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)

        item1 = QtWidgets.QTableWidgetItem(itemname)
        item2 = QtWidgets.QTableWidgetItem(self.parent.state.items[itemname])

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)

    def populateTable(self):
        self.table.setRowCount(0)
        for name in self.parent.state.items:
            self.addRow(name)
