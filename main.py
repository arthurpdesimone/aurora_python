"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from panda3d.core import LVecBase3f

from view.App import *
from view.Geometry import makeSquare, makeCube, logRender
from view.UCS import UCS
from view.UserInterface import *
from view.Grid import *
from view.Tooltip import *
from view.Distance import *
from view.Camera import *


if __name__ == "__main__":
    app = App()
    UserInterface(app)
    ucs = UCS(app)
    Grid(app)
    distance = Distance(app, ucs)
    Tooltip(distance).show()
    CameraController(app)
    faces = makeCube(0.5,0.5,0.5,2,2,2,app.render)


    logRender(app.render)
    app.run()
