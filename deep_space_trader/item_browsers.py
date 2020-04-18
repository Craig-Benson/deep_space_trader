from deep_space_trader.transaction_dialogs import Buy, Sell, PlayerToWarehouse, WarehouseToPlayer
from deep_space_trader.store import Store
from deep_space_trader.utils import errorDialog

from PyQt5 import QtWidgets, QtCore, QtGui


class ItemBrowser(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ItemBrowser, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout(self)

        self.table = QtWidgets.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.setupHeader()
        self.populateTable()
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addWidget(self.table)

        self.table.resizeColumnsToContents()
        self.update()

    def setupHeader(self):
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Item type', 'Quantity'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def update(self):
        self.populateTable()
        super(ItemBrowser, self).update()

    def add_button(self, text, on_click):
        b = QtWidgets.QPushButton(text)
        b.clicked.connect(on_click)
        self.buttonLayout.addWidget(b)

    def addRow(self, itemname):
        raise NotImplementedError()

    def populateTable(self):
        raise NotImplementedError()


class PlayerItemBrowser(ItemBrowser):
    def __init__(self,  *args, **kwargs):
        super(PlayerItemBrowser, self).__init__(*args, **kwargs)

        self.add_button("Sell item", self.sellButtonClicked)
        self.add_button("Add to warehouse", self.warehouseButtonClicked)
        self.add_button("Go to store", self.storeButtonClicked)

    def sellButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, message="Please select an item to sell first!")
            return

        itemname = self.table.item(selectedRow, 0).text()
        if itemname not in self.parent.state.current_planet.items.items:
            errorDialog(self, message="%s is not currently in demand on %s"
                                      % (itemname, self.parent.state.current_planet.full_name))
            return

        dialog = Sell(self.parent, itemname)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def warehouseButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, message="Please select an item first!")
            return

        itemname = self.table.item(selectedRow, 0).text()
        dialog = PlayerToWarehouse(self.parent, itemname)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def storeButtonClicked(self):
        dialog = Store(self.parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def addRow(self, itemname):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)
        collection = self.parent.state.items

        item1 = QtWidgets.QTableWidgetItem(itemname)
        item2 = QtWidgets.QTableWidgetItem(str(collection.items[itemname].quantity))

        item2.setTextAlignment(QtCore.Qt.AlignHCenter)

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)

    def populateTable(self):
        self.table.setRowCount(0)
        for name in self.parent.state.items.items:
            self.addRow(name)


class PlanetItemBrowser(ItemBrowser):
    def __init__(self,  *args, **kwargs):
        super(PlanetItemBrowser, self).__init__(*args, **kwargs)

        self.add_button("Buy item", self.buyButtonClicked)

    def setupHeader(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Item type', 'Quantity', 'Value'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def buyButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, "No item selected",
                        message="Please select an item to buy first!")
            return

        itemname = self.table.item(selectedRow, 0).text()
        if self.parent.state.current_planet.items.items[itemname].quantity == 0:
            errorDialog(self, "None available",
                        message="%s has no %s left to sell" %
                        (self.parent.state.current_planet.full_name, itemname))
            return

        dialog = Buy(self.parent, itemname)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()

    def addRow(self, itemname):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)
        collection = self.parent.state.current_planet.items

        item1 = QtWidgets.QTableWidgetItem(itemname)
        item2 = QtWidgets.QTableWidgetItem(str(collection.items[itemname].quantity))
        item3 = QtWidgets.QTableWidgetItem(str(collection.items[itemname].value))

        item2.setTextAlignment(QtCore.Qt.AlignHCenter)
        item3.setTextAlignment(QtCore.Qt.AlignHCenter)

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)
        self.table.setItem(nextFreeRow, 2, item3)

    def populateTable(self):
        self.table.setRowCount(0)
        for name in self.parent.state.current_planet.items.items:
            self.addRow(name)


class WarehouseItemBrowser(ItemBrowser):
    def __init__(self,  *args, **kwargs):
        super(WarehouseItemBrowser, self).__init__(*args, **kwargs)

        self.add_button("Retrieve from warehouse", self.removeButtonClicked)

    def removeButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, message="Please select an item first!")
            return

        itemname = self.table.item(selectedRow, 0).text()
        dialog = WarehouseToPlayer(self.parent, itemname)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()


    def addRow(self, itemname):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)
        collection = self.parent.state.warehouse

        item1 = QtWidgets.QTableWidgetItem(itemname)
        item2 = QtWidgets.QTableWidgetItem(str(collection.items[itemname].quantity))

        item2.setTextAlignment(QtCore.Qt.AlignHCenter)

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)

    def populateTable(self):
        self.table.setRowCount(0)
        for name in self.parent.state.warehouse.items:
            self.addRow(name)
