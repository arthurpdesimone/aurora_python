import uuid
import requests
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
from qt_material import apply_stylesheet

from tools.Tools import validate_cpf, validate_email, show_error_dialog


class RegisterDialog(QDialog):
    """ Class to define a login dialog to the webserver"""
    def __init__(self, login_dialog):
        super().__init__()
        """ Store a reference from login dialog"""
        self.login_dialog = login_dialog
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
        if not validate_cpf(cpf):
            show_error_dialog("Erro","Digite um CPF válido","CPF inválido")
        if not validate_email(email):
            show_error_dialog("Erro","Digite um e-mail válido","E-mail inválido")

        mac = hex(uuid.getnode())
        auth = {'name': name,
                'email': email,
                'cpf': cpf,
                'mac': mac}
        if validate_cpf(cpf) and validate_email(email):
            data = requests.post("http://127.0.0.1:5000/register", params=auth)
            data_json = data.json()
            if data_json['status'] == 200:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Concluido")
                msg.setInformativeText('A sua serial é: '+data_json['message'])
                msg.setWindowTitle("Serial")
                apply_stylesheet(msg, theme='dark_teal.xml')
                msg.exec()
                self.close()
                self.login_dialog.show()
            else:
                show_error_dialog("Erro", "Ocorreu um erro ao registrar", "Erro no registro")
