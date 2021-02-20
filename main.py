"""
   Aurora python

   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""
from panda3d.core import LVecBase3f

from view.App import *
from view.Geometry import makeSquare
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

    square0 = makeSquare(-1, -1, -1, 1, -1, 1)
    square1 = makeSquare(-1, 1, -1, 1, 1, 1)
    square2 = makeSquare(-1, 1, 1, 1, -1, 1)
    square3 = makeSquare(-1, 1, -1, 1, -1, -1)
    square4 = makeSquare(-1, -1, -1, -1, 1, 1)
    square5 = makeSquare(1, -1, -1, 1, 1, 1)
    snode = GeomNode('square')
    snode.addGeom(square0)
    snode.addGeom(square1)
    snode.addGeom(square2)
    snode.addGeom(square3)
    snode.addGeom(square4)
    snode.addGeom(square5)

    cube = render.attachNewNode(snode)
    cube.setTwoSided(True)

    app.run()
