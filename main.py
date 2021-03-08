# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""

import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from model.Beam import RectangularBeam
from model.Column import RectangularColumn
from model.Footing import ShallowFooting
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

    world = World()
    window = UserInterface()
    window.initialize(world)
    ucs = UCS(world)
    Grid(world)
    distance = Distance(world, ucs, window)
    Camera(world)



    # footing = ShallowFooting(0.5,2,0.25,0.25,0,0.1,0.5,2,2)
    # footing.draw(world.render)
    # beam = RectangularBeam(0.4, 0.19, 1, 1 , 0, 3)
    # beam.draw(world.render)
    # column = RectangularColumn(1,1,1.5,3,0.2,0.2)
    # column.draw(world.render)

    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()

    aspectRatio = world.showbase.getAspectRatio()
    ySize = 1
    xSize = ySize * aspectRatio
    log.appendLog("[" + str(xSize) + "," + str(ySize) + "]")

    log.appendLog('Program finished')
    sys.exit(app.exec_())
