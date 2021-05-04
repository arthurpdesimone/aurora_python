
import uuid
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QDialog
from qt_material import apply_stylesheet


class LoginDialog(QDialog):
    """ Class to define a login dialog to the webserver"""
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme='dark_teal.xml')
        self.main = uic.loadUi('login.ui', self)
        self.main.button_ok.clicked.connect(self.login)
        self.exec_()

    def login(self):
        """ Method to validate serial keys and load the program"""
        serial = self.main.text_serial_key.toPlainText()
        mac = hex(uuid.getnode())
        auth = {'serial':serial,'mac':mac}
        data = requests.post("http://127.0.0.1:5000/login",params =auth )
        print(data.text)





