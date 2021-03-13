# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from database.DatabaseManager import DatabaseManager
from model.Beam import RectangularBeam
from model.Column import RectangularColumn
from model.Footing import ShallowFooting
from view.AxisTripod import AxisTripod
from view.Camera import Camera
from view.Distance import Distance
from view.Grid import Grid
from view.UCS import UCS
from view.UserInterface import UserInterface
from view.World import World
from view.tools.Log import Log

if __name__ == "__main__":
    log = Log.instance()
    log.appendLog('Program started')
    app = QApplication(sys.argv)
    """ Initialize User Interface """
    world = World()
    window = UserInterface()
    window.initialize(world)
    ucs = UCS(world)
    Grid(world)
    distance = Distance(world, ucs, window)
    Camera(world)
    """ Database initialization """
    DatabaseManager('untitled.json')
    """ Add UCS attached to rotation of the model """
    tripod = AxisTripod(world)
    tripod.model.set_compass(world.render)

    """ Qt initialization """
    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()


    log.printRenderChild(world.render)

    log.appendLog('Program finished')
    sys.exit(app.exec_())
