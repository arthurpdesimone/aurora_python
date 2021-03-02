from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QFileDialog
from QPanda3D.QPanda3DWidget import QPanda3DWidget
from qt_material import QtStyleTools

from dxf.DXF import DXF


class UserInterface(QtWidgets.QMainWindow, QtStyleTools):
    def __init__(self):
        super(UserInterface, self).__init__()  # Call the inherited classes __init__ method

    def initialize(self, world):
        self.main = uic.loadUi('window.ui', self)  # Load the .ui file
        self.showbase = world.showbase
        """ Place Panda Qt Widget"""
        layouts = self.findChildren(QWidget, 'visualization')
        layout = layouts[0]
        widget = QPanda3DWidget(world)
        layout.layout().addWidget(widget)
        world.set_parent(layout)


        """ Close menu """
        menu = self.menu_load_dxf
        menu.triggered.connect(self.show_import_dialog_dxf)

    def update_tooltip(self,point):
        self.setToolTip(point)

    def show_import_dialog_dxf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Importar DXF", "", "DXF Files (*.dxf)", options=options)
        if fileName:
            DXF(self.showbase).read_dxf(fileName)
