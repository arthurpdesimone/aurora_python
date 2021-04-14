from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog
from QPanda3D.QPanda3DWidget import QPanda3DWidget
from qt_material import QtStyleTools

from view.gui.ImportDialogDXF import ImportDialogDXF
from view.tools.Log import Log


class UserInterface(QtWidgets.QMainWindow, QtStyleTools):
    log = Log.instance()

    """ Class to manage the user interface"""
    def __init__(self):
        super(UserInterface, self).__init__()  # Call the inherited classes __init__ method

    def initialize(self, world):
        """ Method to open and attach panda3d widget to UI"""
        self.main = uic.loadUi('window.ui', self)  # Load the .ui file
        self.showbase = world.showbase
        """ Place Panda Qt Widget"""
        layouts = self.findChildren(QWidget, 'visualization')
        layout = layouts[0]
        widget = QPanda3DWidget(world)
        layout.layout().addWidget(widget)
        world.set_parent(layout)
        """ Setup menus """
        self.setup_menu()
        """ Setup log text """
        log_text = self.log_text_edit
        self.log.sync_text_area(log_text)

    def setup_menu(self):
        """ Close menu """
        menu = self.menu_load_dxf
        menu.triggered.connect(self.show_import_dialog_dxf)

    def update_statusbar(self, point):
        self.statusBar().showMessage("Mouse position : "+point)

    def show_import_dialog_dxf(self):
        """ Method to show dialog to open a dialog to import DXF files"""
        ImportDialogDXF(self.showbase)