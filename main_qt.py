# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from PyQt5 import QtWidgets, uic
from QPanda3D.QPanda3DWidget import QPanda3DWidget
# import PyQt5 stuff
from PyQt5.QtWidgets import *
import sys

from qt_material import apply_stylesheet

from view.Camera import CameraController
from view.Distance import Distance
from view.Grid import Grid
from view.UCS import UCS
from view.World import World


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method

    def initialize(self,world):
        uic.loadUi('window.ui', self)  # Load the .ui file
        layouts = self.findChildren(QVBoxLayout, 'visualization_layout')
        vlayout = layouts[0]
        widget = QPanda3DWidget(world)
        vlayout.addWidget(widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    world = World()
    window = Ui()
    ucs = UCS(world)
    Grid(world)
    distance = Distance(world, ucs)
    CameraController(world)


    window.initialize(world)
    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()
    app.exec_()
    sys.exit(app.exec_())
