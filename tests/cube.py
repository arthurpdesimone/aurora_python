#!/usr/bin/env python

# Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
# Date: 8/02/2005
#
# This is meant to be a simple example of how to draw a cube
# using Panda's new Geom Interface. Quads arent directly supported
# since they get broken down to trianlges anyway.
#

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LVector3
import sys
import os

base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -10, 0)



# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

def makeSquare(x1, y1, z1, x2, y2, z2):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    #color.addData4f(1.0, 0.0, 0.0, 1.0)
    #color.addData4f(0.0, 1.0, 0.0, 1.0)
    #color.addData4f(0.0, 0.0, 1.0, 1.0)
    #color.addData4f(1.0, 0.0, 1.0, 1.0)

    #texcoord.addData2f(0.0, 1.0)
    #texcoord.addData2f(0.0, 0.0)
    #texcoord.addData2f(1.0, 0.0)
    #texcoord.addData2f(1.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square

# Note: it isn't particularly efficient to make every face as a separate Geom.
# instead, it would be better to create one Geom holding all of the faces.
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

# OpenGl by default only draws "front faces" (polygons whose vertices are
# specified CCW).
cube.setTwoSided(True)

base.run()