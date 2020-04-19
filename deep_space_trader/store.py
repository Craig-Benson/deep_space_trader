import copy
import random
from deep_space_trader.utils import errorDialog, infoDialog, yesNoDialog
from deep_space_trader.location_picker import PlanetDestructionPicker
from deep_space_trader import constants as const

from PyQt5 import QtWidgets, QtCore, QtGui


class StoreItem(object):
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


class PlanetExploration(StoreItem):
    def __init__(self):
        price = const.PLANET_EXPLORATION_COST
        name = "Planet discovery expedition"
        desc = (
            "Allows you to mount an expedition to discover new planets"
        )

        super(PlanetExploration, self).__init__(name, desc, price)

    def use(self, parent):
        ret = yesNoDialog(parent, "Explore?", "Commence exploration for new undiscovered "
                                            "planets with intelligent life? (cost: %d)"
                                            % self.price)

        if not ret:
            return

        num_new = random.randrange(*const.PLANET_DISCOVERY_RANGE)
        parent.state.expand_planets(num_new)

        new_names = [p.full_name for p in parent.state.planets[-num_new:]]
        name_listing = '<br>'.join(new_names)

        infoDialog(parent, "%d new planets with intelligent life have "
                         "been discovered!<br><br>%s" % (num_new, name_listing))

        parent.infoBar.update()
        parent.locationBrowser.update()


class PlanetDestruction(StoreItem):
    def __init__(self):
        price = const.PLANET_DESTRUCTION_COST
        name = "Planet destruction kit"
        desc = (
            "Allows you to destroy a planet and gain all of its resources"
        )

        super(PlanetDestruction, self).__init__(name, desc, price)

    def use(self, parent):
        dialog = PlanetDestructionPicker(parent)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()


store_items = [
    PlanetExploration(),
    PlanetDestruction()
]


class Store(QtWidgets.QDialog):
    def __init__(self, parent):
        super(Store, self).__init__(parent)

        self.parent = parent
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        buttonLayout = QtWidgets.QHBoxLayout()

        self.buyButton = QtWidgets.QPushButton("Buy item")
        self.buyButton.clicked.connect(self.buyButtonClicked)
        buttonLayout.addWidget(self.buyButton)

        self.moneyLabel = QtWidgets.QLabel()
        self.updateMoneyLabel()
        buttonLayout.addWidget(self.moneyLabel)

        self.mainLayout.addLayout(buttonLayout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Item', 'description', 'Price'])
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.setWordWrap(True)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.table.resizeRowsToContents()

        self.mainLayout.addWidget(self.table)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Store")

        self.update()

    def updateMoneyLabel(self):
        self.moneyLabel.setText("Your money: %d" % self.parent.state.money)

    def addRow(self, item):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)

        item1 = QtWidgets.QTableWidgetItem(item.name)
        item2 = QtWidgets.QTableWidgetItem(item.description)
        item3 = QtWidgets.QTableWidgetItem(str(item.price))

        item3.setTextAlignment(QtCore.Qt.AlignHCenter)

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)
        self.table.setItem(nextFreeRow, 2, item3)

    def populateTable(self):
        self.table.setRowCount(0)
        for item in store_items:
            self.addRow(item)

    def update(self):
        self.populateTable()
        super(Store, self).update()

    def playerHasItem(self, name):
        for item in self.parent.state.store_items:
            if item.name == name:
                return True

        return False

    def buyButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            errorDialog(self, message="Please select an item first")
            return

        item = store_items[selectedRow]
        if self.playerHasItem(item.name):
            errorDialog(self, message="You already have 1 '%s', you must use "
                                      " it before you can buy another" % item.name)
            return

        if self.parent.state.money < item.price:
            errorDialog(self, message="You don't have enough money to buy '%s'" % item.name)
            return

        self.parent.state.money -= item.price
        self.parent.state.store_items.append(copy.deepcopy(item))
        self.updateMoneyLabel()
        self.parent.infoBar.update()

        infoDialog(self, message="You purchased '%s'" % item.name)

    def sizeHint(self):
        return QtCore.QSize(800, 400)
