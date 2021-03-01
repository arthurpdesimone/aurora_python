# -*- coding: utf-8-*-
"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""

import sys

from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from view.Camera import Camera
from view.Distance import Distance
from view.Grid import Grid
from view.Tooltip import Tooltip
from view.UCS import UCS
from view.Ui import Ui
from view.World import World

if __name__ == "__main__":
    app = QApplication(sys.argv)

    world = World()
    window = Ui()
    window.initialize(world)
    ucs = UCS(world)
    Grid(world)
    distance = Distance(world, ucs)
    Camera(world)



    apply_stylesheet(window, theme='dark_teal.xml')
    window.showMaximized()
    window.show()

    sys.exit(app.exec_())
