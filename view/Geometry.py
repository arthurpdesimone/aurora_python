from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, LVector3, Geom, GeomTriangles, LVecBase4f


def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec


def makeSquare(x1, y1, z1, x2, y2, z2, color_square=LVecBase4f(1, 0, 0, 1)):
    """
    Method to draw a square using two triangles

    :param x1: the first lower left x coordinate
    :type x1: float
    :param y1: the first lower left x coordinate
    :type y1: float
    :param z1: the first lower left x coordinate
    :type z1: float
    :param x2: the first lower left x coordinate
    :type x2: float
    :param y2: the first lower left x coordinate
    :type y2: float
    :param z2: the first lower left x coordinate
    :type z2: float
    :param color_square: the square's color in RGBA vector form
    :type color_square: panda.core.LVecBase4f
    """

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
    color.addData4f(color_square)
    color.addData4f(color_square)
    color.addData4f(color_square)
    color.addData4f(color_square)

    # texcoord.addData2f(0.0, 1.0)
    # texcoord.addData2f(0.0, 0.0)
    # texcoord.addData2f(1.0, 0.0)
    # texcoord.addData2f(1.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)

    return square
