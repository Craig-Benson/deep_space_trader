from PyQt5 import QtWidgets, QtCore, QtGui


class Buy(QtWidgets.QDialog):
    def __init__(self, parent, itemname):
        super(Buy, self).__init__(parent=parent)

        self.parent = parent
        self.value = parent.state.current_planet.items.items[itemname].value
        self.capacity = parent.state.capacity - parent.state.items.count()
        self.itemName = itemname
        mainLayout = QtWidgets.QVBoxLayout(self)
        spinboxLayout = QtWidgets.QHBoxLayout()
        buttonLayout = QtWidgets.QHBoxLayout()

        description = QtWidgets.QLabel("How much %s do you want to buy?" % itemname)
        moneyCount = QtWidgets.QLabel("(your money: %d)" % parent.state.money)

        self.spinboxLabel = QtWidgets.QLabel("")
        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.valueChanged.connect(self.valueChanged)

        max_buy = int(parent.state.money / self.value)
        self.spinbox.setMaximum(min(max_buy, self.capacity))

        spinboxLayout.addWidget(self.spinboxLabel)
        spinboxLayout.addWidget(self.spinbox)

        buyButton = QtWidgets.QPushButton("Buy")
        buyButton.clicked.connect(self.buyButtonClicked)
        buttonLayout.addWidget(buyButton)

        cancelButton = QtWidgets.QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelButtonClicked)
        buttonLayout.addWidget(cancelButton)

        mainLayout.addWidget(description)
        mainLayout.addWidget(moneyCount)
        mainLayout.addLayout(spinboxLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Buy items")

        self.valueChanged()

    def buyButtonClicked(self):
        quantity = int(self.spinbox.value())
        self.parent.state.items.add_items(self.itemName,
                                          self.parent.state.current_planet.items,
                                          quantity)

        cost = self.parent.state.current_planet.items.items[self.itemName].value * quantity
        self.parent.state.money -= cost
        self.parent.playerItemBrowser.update()
        self.parent.planetItemBrowser.update()
        self.parent.infoBar.update()
        self.accept()

    def cancelButtonClicked(self):
        self.reject()

    def valueChanged(self):
        self.spinboxLabel.setText("Buy quantity (cost: %s)"
                                  % (self.spinbox.value() * self.value))
