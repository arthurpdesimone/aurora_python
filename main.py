# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""

import sys

from PyNite.Node3D import Node3D
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from database.DatabaseManager import DatabaseManager
from lang.Language import PROGRAM_STARTED, PROGRAM_LOADED
from model.Beam import Beam
from model.Column import RectangularColumn
from model.Footing import ShallowFooting
from model.Model import Model
from view.AxisTripod import AxisTripod
from view.Camera import Camera
from view.Distance import Distance
from view.Grid import Grid
from view.UCS import UCS
from view.UserInterface import UserInterface
from view.World import World
from view.gui.CreateFileDialog import CreateFileDialog
from view.gui.LoginDialog import LoginDialog
from view.tools.Log import Log


if __name__ == "__main__":
    app = QApplication(sys.argv)
    """ Initialize User Interface """
    login = LoginDialog()
    world = World()
    window = UserInterface()
    window.initialize(world)
    log = Log.instance()
    log.appendLog(PROGRAM_STARTED)

    ucs = UCS(world)
    Grid(world)
    distance = Distance(world, ucs, window)
    Camera(world)

    """ Add UCS attached to rotation of the model """
    tripod = AxisTripod(world)
    tripod.model.set_compass(world.render)
    # """Types testing"""
    # initial_node = Node3D("test1",0,0,0)
    # end_node = Node3D("test2", 1, 1, 1)
    # b = Beam(initial_node,end_node)

    """ Qt initialization """
    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()
    #log.printRenderChild(world.render)
    log.appendLog(PROGRAM_LOADED)

    window.check_model_existence()

    sys.exit(app.exec_())
