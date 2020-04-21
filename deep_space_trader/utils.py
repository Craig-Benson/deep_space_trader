import hashlib
import base64

from PyQt5 import QtWidgets


_pwd = b'g\x54n70erew feasf90s gf\xff\x0f\x290780 9\x02ng7804\x00>:": k'


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


def _add_wrap(v, a, w):
    return (v + a) % w

def _sub_wrap(v, s, w):
    if s > v:
        return w - (s - v)
    else:
        return v - s


def _iter_bytes(data, byte_func):
    ret = bytearray(data)
    i = 0
    j = 0

    pwd_rounds = 0
    data_rounds = 0

    while (data_rounds < 100) and (pwd_rounds < 100):
        ret[i] = byte_func(ret[i], _pwd[j], 256)

        if i < (len(data) - 1):
            i += 1
        else:
            i = 0
            data_rounds += 1

        if j < (len(_pwd) - 1):
            j += 1
        else:
            j = 0
            pwd_rounds += 1

    return bytes(ret)

# note: scores_encode is not cryptographically secure by any means. It is
# a simple byte-scrambling function to prevent shared high scores from being
# easily modified, but I'm sure someone who really wanted could easily crack it

def scores_encode(data):
    return base64.b64encode(_iter_bytes(data, _add_wrap))

def scores_decode(data):
    return _iter_bytes(base64.b64decode(data), _sub_wrap)
