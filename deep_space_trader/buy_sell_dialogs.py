from PyQt5 import QtWidgets, QtCore, QtGui


class BuySellDialog(QtWidgets.QDialog):
    def __init__(self, parent, itemname, include_money=True):
        super(BuySellDialog, self).__init__(parent=parent)

        self.parent = parent
        self.itemName = itemname
        mainLayout = QtWidgets.QVBoxLayout(self)
        spinboxLayout = QtWidgets.QHBoxLayout()
        buttonLayout = QtWidgets.QHBoxLayout()

        self.description = QtWidgets.QLabel()
        moneyCount = QtWidgets.QLabel("(your money: %d)" % parent.state.money)

        self.spinboxLabel = QtWidgets.QLabel("")
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.valueChanged.connect(self.valueChanged)
        self.spinbox.setMaximum(self.maximumQuantity())

        maxButton = QtWidgets.QPushButton("Max")
        maxButton.clicked.connect(self.maxButtonClicked)

        spinboxLayout.addWidget(self.spinboxLabel)
        spinboxLayout.addWidget(self.spinbox)
        spinboxLayout.addWidget(maxButton)

        self.acceptButton = QtWidgets.QPushButton()
        self.acceptButton.clicked.connect(self.acceptButtonClicked)
        buttonLayout.addWidget(self.acceptButton)

        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelButtonClicked)
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(self.description)

        if include_money:
            mainLayout.addWidget(moneyCount)

        mainLayout.addLayout(spinboxLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Buy items")

        self.valueChanged()

    def maxButtonClicked(self):
        self.spinbox.setValue(self.maximumQuantity())

    def acceptButtonClicked(self):
        self.acceptTransaction(int(self.spinbox.value()))
        self.parent.playerItemBrowser.update()
        self.parent.planetItemBrowser.update()
        self.parent.infoBar.update()
        self.accept()

    def cancelButtonClicked(self):
        self.reject()

    def acceptTransaction(self, quantity):
        raise NotImplementedError()

    def valueChanged(self):
        raise NotImplementedError()

    def maximumQuantity(self):
        raise NotImplementedError()


class Buy(BuySellDialog):
    def __init__(self, parent, itemname):
        self.value = parent.state.current_planet.items.items[itemname].value
        self.quantity = parent.state.current_planet.items.items[itemname].quantity

        super(Buy, self).__init__(parent, itemname, include_money=True)

        self.description.setText("How much %s do you want to buy?" % self.itemName)
        self.acceptButton.setText("Buy")

    def acceptTransaction(self, quantity):
        self.parent.state.items.add_items(self.itemName,
                                          self.parent.state.current_planet.items,
                                          quantity)

        self.parent.state.money -= self.value * quantity

    def valueChanged(self):
        self.spinboxLabel.setText("Buy quantity (cost: %s)"
                                  % (self.spinbox.value() * self.value))

    def maximumQuantity(self):
        capacity = self.parent.state.capacity - self.parent.state.items.count()
        max_buy = int(self.parent.state.money / self.value)
        return min(max_buy, capacity, self.quantity)

    def sourceCollection(self):
        return self.parent.state.current_planet.items


class Sell(BuySellDialog):
    def __init__(self, parent, itemname):
        self.value = parent.state.current_planet.items.items[itemname].value
        self.quantity = parent.state.items.items[itemname].quantity

        super(Sell, self).__init__(parent, itemname, include_money=True)
        self.description.setText("How much %s do you want to sell?" % self.itemName)
        self.acceptButton.setText("Sell")

    def acceptTransaction(self, quantity):
        self.parent.state.current_planet.items.add_items(self.itemName,
                                                         self.parent.state.items,
                                                         quantity)

        self.parent.state.money += self.value * quantity

    def valueChanged(self):
        self.spinboxLabel.setText("Sell quantity (gain: %s)"
                                  % (self.spinbox.value() * self.value))

    def maximumQuantity(self):
        return self.quantity
