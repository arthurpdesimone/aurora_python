# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from PyQt5 import QtWidgets, uic
from QPanda3D.Panda3DWorld import Panda3DWorld
from QPanda3D.QPanda3DWidget import QPanda3DWidget
# import PyQt5 stuff
from PyQt5.QtWidgets import *
import sys

from pandac.PandaModules import Point3, Vec3, Vec4, VBase4
from qt_material import apply_stylesheet



class PandaTest(Panda3DWorld):
    """
    This is the class that defines our world
    It inherits from Panda3DWorld that inherits from
    Panda3D's ShowBase class
    """

    def __init__(self):
        Panda3DWorld.__init__(self)
        self.cam.setPos(0, -28, 6)
        self.win.setClearColorActive(True)
        self.win.setClearColor(VBase4(0, 0.5, 0, 1))
        self.testModel = loader.loadModel('panda')
        self.testModel.reparentTo(render)

        # This rotates the actor 180 degrees on heading and 90 degrees on pitch.
        myInterval4 = self.testModel.hprInterval(1.0, Vec3(360, 0, 0))
        myInterval4.loop()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('../window.ui', self) # Load the .ui file
        layouts = self.findChildren(QVBoxLayout, 'visualization_layout')
        vlayout = layouts[0]
        vlayout.addWidget(QPanda3DWidget(PandaTest()))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()
    app.exec_()
    sys.exit(app.exec_())
