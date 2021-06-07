import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QMessageBox,QCompleter
from QPanda3D.QPanda3DWidget import QPanda3DWidget
from direct.showbase.MessengerGlobal import messenger
from qt_material import QtStyleTools

from lang.Language import *
from model.Model import Model
from model.command.Commands import commands
from view.gui.CreateFileDialog import CreateFileDialog
from view.gui.HotkeyDialog import HotkeyDialog
from view.gui.ImportDialogDXF import ImportDialogDXF
from view.gui.OpenFileDialog import OpenFileDialog
from view.tools.Log import Log


class UserInterface(QtWidgets.QMainWindow, QtStyleTools):
    log = Log.instance()

    """ Class to manage the user interface"""
    def __init__(self,world):
        super(UserInterface, self).__init__()  # Call the inherited classes __init__ method
        self.world = world
        self.initialize()

    def initialize(self):
        """ Method to open and attach panda3d widget to UI"""
        self.main = uic.loadUi('window.ui', self)  # Load the .ui file
        self.showbase = self.world.showbase
        """ Place Panda Qt Widget"""
        layouts = self.findChildren(QWidget, 'visualization')
        layout = layouts[0]
        widget = QPanda3DWidget(self.world,debug=True)
        layout.layout().addWidget(widget)
        self.world.set_parent(layout)
        """ Create autocompleter on command """
        completer = QCompleter(commands)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.command_line.setCompleter(completer)
        self.command_line.returnPressed.connect(self.parse_command)
        """ Setup menus """
        self.setup_menu()
        """ Setup log text """
        log_text = self.log_text_edit
        self.log.sync_text_area(log_text)
        """ Show hotkey help"""
        self.show_hotkey_dialog()

    def check_model_existence(self):
        """ Prompt the user if he wants to create a new file, if so opens a dialog"""
        reply = QMessageBox.question(self, 'Criar arquivo',
                                           "Deseja criar um novo arquivo?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            """ Database initialization """
            dialog = CreateFileDialog()
            file = dialog.file
            if file == "":
                sys.exit()
            else:
                if ".json" not in file: file = file + ".json"
                self.create_or_open_file(file)

    def open_file(self):
        """ Open file method"""
        dialog = OpenFileDialog()
        file = dialog.file
        if file != "":
            self.create_or_open_file(file)

    def create_or_open_file(self, file):
        """ Create or open file method, including database initialization"""
        model = Model.instance()
        model.init_db(file)
        self.log.appendLog(FILE_OPENED + file)
        self.main.setWindowTitle("Aurora - " + file)

    def setup_menu(self):
        """ Configure menus"""
        """ New file"""
        menu_new = self.menu_new
        menu_new.triggered.connect(self.check_model_existence)
        """ New file"""
        menu_open = self.menu_open
        menu_open.triggered.connect(self.open_file)
        """ Import DXF file"""
        menu_load_dxf = self.menu_load_dxf
        menu_load_dxf.triggered.connect(self.show_import_dialog_dxf)

    def update_statusbar(self, point):
        self.statusBar().showMessage("Mouse position : "+point)

    def show_import_dialog_dxf(self):
        """ Method to show dialog to open a dialog to import DXF files"""
        ImportDialogDXF(self.showbase)

    def show_hotkey_dialog(self):
        hotkey_dialog = HotkeyDialog()
        hotkey_dialog.show()

    def parse_command(self):
        """ Parse command according to the text at the command line"""
        command = self.command_line.text()
        self.log.appendLog(command)
        """ Command switch"""
        if command == "CAMERA_DESLIGAR":
            messenger.send("remove_camera")
        elif command == "CAMERA_LIGAR":
            messenger.send("accept_camera")
        elif command == "LINHA":
            messenger.send("line")

        self.command_line.setText("")