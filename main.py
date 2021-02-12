"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from view.app import *
from view.userinterface import *
from view.grid import *
from view.tooltip import *
from view.distance import *
from view.camera import *


if __name__ == "__main__":
    app = App()
    UserInterface(app)
    ucs = UCS(app)
    Grid(app)
    distance = Distance(app, ucs)
    Tooltip(distance).show()
    CameraController(app)
    app.run()
