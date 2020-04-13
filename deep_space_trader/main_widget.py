import os
import json
import zlib
import copy
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui

from deep_space_trader.utils import yesNoDialog, errorDialog
from deep_space_trader.game_state import State
from deep_space_trader.location_browser import LocationBrowser
from deep_space_trader.item_browsers import PlayerItemBrowser, PlanetItemBrowser, WarehouseItemBrowser
from deep_space_trader.information_bar import InfoBar


# Set checkbox state without triggering the stateChanged signal
def _silent_checkbox_set(checkbox, value, handler):
    checkbox.stateChanged.disconnect(handler)
    checkbox.setChecked(value)
    checkbox.stateChanged.connect(handler)

class MainWidget(QtWidgets.QDialog):
    def __init__(self, primaryScreen, mainWindow):
        super(MainWidget, self).__init__()

        self.main = mainWindow
        self.primary_screen = primaryScreen
        self.state = State()

        middleColumnLayout = QtWidgets.QHBoxLayout()

        planetsLayout = QtWidgets.QHBoxLayout()
        planetsLayout.addWidget(LocationBrowser(self))
        locationBrowserGroup = QtWidgets.QGroupBox("planets")
        locationBrowserGroup.setAlignment(QtCore.Qt.AlignCenter)
        locationBrowserGroup.setLayout(planetsLayout)
        middleColumnLayout.addWidget(locationBrowserGroup)

        playerItemsLayout = QtWidgets.QHBoxLayout()
        playerItemsLayout.addWidget(PlayerItemBrowser(self))
        self.playerItemBrowserGroup = QtWidgets.QGroupBox()
        self.playerItemBrowserGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.playerItemBrowserGroup.setLayout(playerItemsLayout)
        self.updatePlayerItemsLabel()
        middleColumnLayout.addWidget(self.playerItemBrowserGroup)

        infoLayout = QtWidgets.QHBoxLayout()
        infoLayout.addWidget(InfoBar(self))
        infoGroup = QtWidgets.QGroupBox("Information")
        infoGroup.setAlignment(QtCore.Qt.AlignCenter)
        infoGroup.setLayout(infoLayout)

        lastColumnLayout = QtWidgets.QHBoxLayout()

        planetItemsLayout = QtWidgets.QHBoxLayout()
        planetItemsLayout.addWidget(PlanetItemBrowser(self))
        planetItemsBrowserGroup = QtWidgets.QGroupBox("Items on current planet")
        planetItemsBrowserGroup.setAlignment(QtCore.Qt.AlignCenter)
        planetItemsBrowserGroup.setLayout(planetItemsLayout)
        lastColumnLayout.addWidget(planetItemsBrowserGroup)

        warehouseItemsLayout = QtWidgets.QHBoxLayout()
        warehouseItemsLayout.addWidget(WarehouseItemBrowser(self))
        warehouseItemsBrowserGroup = QtWidgets.QGroupBox("Items in warehouse")
        warehouseItemsBrowserGroup.setAlignment(QtCore.Qt.AlignCenter)
        warehouseItemsBrowserGroup.setLayout(warehouseItemsLayout)
        lastColumnLayout.addWidget(warehouseItemsBrowserGroup)


        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(infoGroup)
        self.mainLayout.addLayout(middleColumnLayout)
        self.mainLayout.addLayout(lastColumnLayout)

    def updatePlayerItemsLabel(self):
        self.playerItemBrowserGroup.setTitle("Your items (%d/%d)" %
                                             (self.state.items.count(),
                                             self.state.capacity))

    def warningBeforeQuit(self):
        return yesNoDialog(self, "Are you sure?", "Are you sure you want to quit?"
                                 " You will lose any unsaved data.")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            # If we're in the middle of a move/copy operation, escape key should cancel it
            if self.tracking_tile_button_enter:
                self.eraseSelectionMask()
                self.tracking_tile_button_enter = False
                self.group_mask = []

            # Otherwise, escape key should close the main window (after a warning)
            else:
                if self.warningBeforeQuit():
                    QtWidgets.qApp.quit()


        self.enableSelectionDependentItems()
