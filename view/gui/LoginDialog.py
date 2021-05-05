
import uuid
import requests
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog
from qt_material import apply_stylesheet

from tools.Tools import show_error_dialog
from view.gui.RegisterDialog import RegisterDialog


class LoginDialog(QDialog):
    """ Class to define a login dialog to the webserver"""
    def __init__(self, main_window):
        super().__init__()
        """ Store a reference to the main window"""
        self.main_window = main_window
        apply_stylesheet(self, theme='dark_teal.xml')
        """Define maximum length of the serial key field"""
        self.main = uic.loadUi('login.ui', self)
        self.main.text_serial_key.textChanged.connect(self.txtInputChanged)
        self.main.button_ok.clicked.connect(self.login)
        self.main.button_register.clicked.connect(self.register)
        """ Disable close and help upper buttons"""
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.exec_()

    def txtInputChanged(self):
        """ Maximum length of serial field and right format"""
        if len(self.main.text_serial_key.toPlainText()) > 12:
            text = self.main.text_serial_key.toPlainText()
            text = text[:12]
            self.main.text_serial_key.setPlainText(text.upper())
            cursor = self.main.text_serial_key.textCursor()
            cursor.setPosition(12)
            self.main.text_serial_key.setTextCursor(cursor)

    def login(self):
        """ Method to validate serial keys and load the program"""
        try:
            serial = self.main.text_serial_key.toPlainText()
            mac = hex(uuid.getnode())
            auth = {'serial':serial,'mac':mac}
            data = requests.post("http://127.0.0.1:5000/login",params =auth)
            data_json = data.json()
            if data_json['status'] == 200:
                self.close()
                self.main_window.showMaximized()
                self.main_window.show()
            elif data_json['status'] == 403:
                show_error_dialog("Serial invalida ou computador não registrado",
                                  "Erro","Erro")

        except Exception as e:
            print(e)
            pass

    def register(self):
        self.hide()
        RegisterDialog(self)





