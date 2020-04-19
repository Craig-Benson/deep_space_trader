from deep_space_trader.store import Store
from deep_space_trader import constants as const
from deep_space_trader import config
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

    def checkHighScore(self):
        scores = config.highscores()

        # High scores are sorted in descending order
        if (len(scores) > 0) and (self.parent.state.money <= scores[0][1]):
            return

        proceed = yesNoDialog(self, "High score!",
                              message="You have achieved a high score (%d) ! "
                                      "would you like to enter your name? (high "
                                      "scores are only stored locally)" % self.parent.state.money)

        if not proceed:
            return

        name = None

        while True:
            name, accepted = QtWidgets.QInputDialog.getText(self, 'Enter name',
                                                            "Enter your name for the high score table")

            if not accepted:
                return

            if len(name) > const.MAX_HIGHSCORE_NAME_LEN:
                errorDialog(self, "Too long", "Name is too long (max %d characters)"
                                  % const.MAX_HIGHSCORE_NAME_LEN)
            else:
                break

        config.add_highscore(name, self.parent.state.money)
        config.config_store()
        self.parent.showHighScores()

    def dayButtonClicked(self):
        if self.parent.state.next_day():
            # Days remaining
            self.parent.infoBar.update()
            self.parent.planetItemBrowser.update()
        else:
            # No days remaining
            infoDialog(self, "Game complete", message="You are done")

            self.checkHighScore()

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
