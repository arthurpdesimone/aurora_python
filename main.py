"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from panda3d.core import LVecBase3f

from model.Beam import Beam, RectangularBeam
from model.Column import RectangularColumn
from model.Footing import ShallowFooting
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

    #footing = ShallowFooting(0.5,2,0.25,0.25,0,0.1,0.5,2,2)
    #footing.draw(app.render)
    #beam = RectangularBeam(0.4, 0.19, 1, 1 , 0, 3)
    #beam.draw(app.render)
    #column = RectangularColumn(1,1,1.5,3,0.2,0.2)
    #column.draw(app.render)

    logRender(app.render)
    app.run()
