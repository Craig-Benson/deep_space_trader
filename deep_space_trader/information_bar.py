from PyQt5 import QtWidgets, QtCore, QtGui


class InfoBar(QtWidgets.QWidget):
    def __init__(self, parent):
        super(InfoBar, self).__init__(parent)

        self.parent = parent

        moneyLayout = QtWidgets.QHBoxLayout()
        self.moneyLabel = QtWidgets.QLabel("")
        self.moneyLabel.setAlignment(QtCore.Qt.AlignCenter)
        moneyLayout.addWidget(self.moneyLabel)
        moneyGroup = QtWidgets.QGroupBox("Money")
        moneyGroup.setAlignment(QtCore.Qt.AlignCenter)
        moneyGroup.setLayout(moneyLayout)

        planetCountLayout = QtWidgets.QHBoxLayout()
        self.planetCountLabel = QtWidgets.QLabel("")
        self.planetCountLabel.setAlignment(QtCore.Qt.AlignCenter)
        planetCountLayout.addWidget(self.planetCountLabel)
        planetCountGroup = QtWidgets.QGroupBox("Planets discovered")
        planetCountGroup.setAlignment(QtCore.Qt.AlignCenter)
        planetCountGroup.setLayout(planetCountLayout)

        capacityLayout = QtWidgets.QHBoxLayout()
        self.capacityLabel = QtWidgets.QLabel("")
        self.capacityLabel.setAlignment(QtCore.Qt.AlignCenter)
        capacityLayout.addWidget(self.capacityLabel)
        capacityGroup = QtWidgets.QGroupBox("Capacity")
        capacityGroup.setAlignment(QtCore.Qt.AlignCenter)
        capacityGroup.setLayout(capacityLayout)

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.addWidget(moneyGroup)
        self.mainLayout.addWidget(planetCountGroup)
        self.mainLayout.addWidget(capacityGroup)
        self.update()

    def update(self):
        self.moneyLabel.setText(str(self.parent.state.money))
        self.planetCountLabel.setText(str(len(self.parent.state.planets)))
        self.capacityLabel.setText(str(self.parent.state.capacity))
        super(InfoBar, self).update()
