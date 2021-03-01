from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget
from QPanda3D.QPanda3DWidget import QPanda3DWidget


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method

    def initialize(self, world):
        uic.loadUi('window.ui', self)  # Load the .ui file

        """ Place Panda Qt Widget"""
        layouts = self.findChildren(QWidget, 'visualization')
        layout = layouts[0]
        widget = QPanda3DWidget(world)
        layout.layout().addWidget(widget)
        world.set_parent(layout)

        """ Close menu """
        menu = self.menu_load_dxf
        menu.triggered.connect(self.show_import_dialog_dxf)

    def show_import_dialog_dxf(self):
        print('Hello')
