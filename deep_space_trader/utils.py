from PyQt5 import QtWidgets


def yesNoDialog(parent, header="", message="Are you sure?"):
    reply = QtWidgets.QMessageBox.question(parent, header, message,
                                           (QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No |
                                           QtWidgets.QMessageBox.Cancel),
                                           QtWidgets.QMessageBox.Cancel)

    return reply == QtWidgets.QMessageBox.Yes

def errorDialog(parent, heading="Error", message="Unrecoverable error occurred"):
    msg = QtWidgets.QMessageBox(parent)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(heading)
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

def infoDialog(parent, heading="", message=""):
    msg = QtWidgets.QMessageBox(parent)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(heading)
    msg.setInformativeText(message)
    msg.setWindowTitle("Information")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

