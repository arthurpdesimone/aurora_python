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
from view.DrawingLine import DrawingLine
from view.Grid import Grid
from view.UCS import UCS
from view.UserInterface import UserInterface
from view.World import World
from view.gui.CreateFileDialog import CreateFileDialog
from view.gui.Themes import DARK_TEAL
from view.tools.Log import Log


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    """ Initialize User Interface """
    world = World()
    window = UserInterface(world)
    log = Log.instance()
    log.appendLog(PROGRAM_STARTED)
    """ Initializing panda3d world with useful graphics"""
    ucs = UCS(world)
    Grid(world)
    Distance(ucs, window)
    Camera()
    DrawingLine(world,window)

    """ Add UCS attached to rotation of the model """
    tripod = AxisTripod(world)
    tripod.model.set_compass(world.render)

    """ Qt initialization """
    apply_stylesheet(window, theme=DARK_TEAL)
    window.showMaximized()
    window.show()
    log.appendLog(PROGRAM_LOADED)

    window.check_model_existence()
    """ https://stackoverflow.com/questions/33736819/pyqt-no-error-msg-traceback-on-exit """
    sys.excepthook = except_hook

    """ App initialization """
    sys.exit(app.exec())
