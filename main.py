"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from view.app import *
from view.gui import *
from view.grid import *
from view.tooltip import *
from view.distance import *
from view.camera import *


if __name__ == "__main__":
    app = App()
    Gui(app)
    ucs = UCS(app)
    Grid(app)
    distance = Distance(app, ucs)
    Tooltip(distance).show()
    CameraController(app)
    app.run()
