import uuid
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog
from qt_material import apply_stylesheet

class RegisterDialog(QDialog):
    """ Class to define a login dialog to the webserver"""
    def __init__(self):
        super().__init__()
        apply_stylesheet(self, theme='dark_teal.xml')
        """Define maximum length of the serial key field"""
        self.main = uic.loadUi('register.ui', self)
        self.main.button_register.clicked.connect(self.register)
        """ Disable close and help upper buttons"""
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.exec_()

    def login(self):
        """ Method to validate serial keys and load the program"""
        try:
            serial = self.main.text_serial_key.toPlainText()
            mac = hex(uuid.getnode())
            auth = {'serial': serial,
                    'mac': mac
                    }
            data = requests.post("http://127.0.0.1:5000/login",params =auth)
            print(data.text)
        except Exception as e:
            print(e)

    def register(self):
        name = self.main.text_name.toPlainText()
        email = self.main.text_email.toPlainText()
        cpf = self.main.text_cpf.toPlainText()
        mac = hex(uuid.getnode())
        auth = {'name': name,
                'email': email,
                'cpf': cpf,
                'mac': mac}
        data = requests.post("http://127.0.0.1:5000/register", params=auth)
        print(data.text)