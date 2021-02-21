from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, LVector3, Geom, GeomTriangles, LVecBase4f, \
    GeomNode, LineSegs, NodePath, Triangulator3, Triangulator


def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec


def makeLine(x1,y1,z1,x2,y2,z2, lineSegs, thickness=1, color_line = LVecBase4f(0.1, 0.1, 0.1, 0.1)):
    """
        Method to draw a line betweeen two points

        :param x1: the first x coordinate
        :type x1: float
        :param y1: the first y coordinate
        :type y1: float
        :param z1: the first z coordinate
        :type z1: float
        :param x2: the second x coordinate
        :type x2: float
        :param y2: the second y coordinate
        :type y2: float
        :param z2: the second z coordinate
        :type z2: float
        :param color_line: the line's color in RGBA vector form
        :type color_line: :class:'panda.core.LVecBase4f'
    """

    ls = lineSegs
    ls.setThickness(thickness)
    ls.setColor(color_line)
    ls.moveTo(x1, y1, z1)
    ls.drawTo(x2, y2, z2)

    return ls


def drawPolygon(points, color_face=LVecBase4f(1, 1, 1, 1)):
    """ Method to draw a polygon based on a set of points CCW oriented

    :param points: A list of points
    :type points: list
    """

    """ Setting parameters to draw a convex polygon"""
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('polygon', format, Geom.UHStatic)
    vdata.setNumRows(len(points))

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    """ Loop through the points adding them to the GeomVertexWriter object
    and adding to the triangulator 
    """
    triangulator = Triangulator3()
    for i, point in enumerate(points):
        print(point)
        x = point[0]
        y = point[1]
        z = point[2]
        vertex.addData3(x, y, z)
        normal.addData3(normalized(2*x-1, 2*y-1, 2*z-1))
        color.addData4(color_face[0], color_face[1], color_face[2], color_face[3])
        triangulator.addVertex(x, y, z)
        # add the vertex index to the polygon
        triangulator.add_polygon_vertex(i)

    triangulator.triangulate()
    print(triangulator.getNumTriangles())

    prim = GeomTriangles(Geom.UHStatic)
    for i in range(triangulator.getNumTriangles()):
        prim.addVertices(triangulator.getTriangleV0(i),
                         triangulator.getTriangleV1(i),
                         triangulator.getTriangleV2(i))
        prim.closePrimitive()


def makeSquare(x1, y1, z1, x2, y2, z2, color_square=LVecBase4f(1, 1, 1, 1)):
    """
    Method to draw a square using two triangles

    :param x1: the first lower left x coordinate
    :type x1: float
    :param y1: the first lower left y coordinate
    :type y1: float
    :param z1: the first lower left z coordinate
    :type z1: float
    :param x2: the first upper left x coordinate
    :type x2: float
    :param y2: the first upper left y coordinate
    :type y2: float
    :param z2: the first upper left z coordinate
    :type z2: float
    :param color_square: the square's color in RGBA vector form
    :type color_square: :class:'panda.core.LVecBase4f'
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


def makeCube(x1, y1, z1, x2, y2, z2, render, color_face=LVecBase4f(1, 1, 1, 1), edge_thickness = 3):
    """
       Method to draw a hollow cube

       :param x1: the first lower left x coordinate
       :type x1: float
       :param y1: the first lower left y coordinate
       :type y1: float
       :param z1: the first lower left z coordinate
       :type z1: float
       :param x2: the first upper left x coordinate
       :type x2: float
       :param y2: the first upper left y coordinate
       :type y2: float
       :param z2: the first upper left z coordinate
       :type z2: float
       :param color_square: the cube's color in RGBA vector form
       :type color_square: :class:'panda.core.LVecBase4f'
    """
    square0 = makeSquare(x1, y1, z1, x2, y1, z2, color_face)
    square1 = makeSquare(x1, y2, z1, x2, y2, z2, color_face)
    square2 = makeSquare(x1, y2, z2, x2, y1, z2, color_face)
    square3 = makeSquare(x1, y2, z1, x2, y1, z1, color_face)
    square4 = makeSquare(x1, y1, z1, x1, y2, z2, color_face)
    square5 = makeSquare(x2, y1, z1, x2, y2, z2, color_face)
    faces = GeomNode('Face')

    edges = LineSegs('Edges')
    """ 1st face """
    edges = makeLine(x1, y1, z1, x1, y1, z2, edges, thickness=edge_thickness)
    edges = makeLine(x1, y1, z2, x2, y1, z2, edges, thickness=edge_thickness)
    edges = makeLine(x1, y1, z1, x2, y1, z1, edges, thickness=edge_thickness)
    edges = makeLine(x2, y1, z1, x2, y1, z2, edges, thickness=edge_thickness)
    """ 2nd face """
    edges = makeLine(x1, y1, z1, x1, y2, z1, edges, thickness=edge_thickness)
    edges = makeLine(x1, y2, z1, x1, y2, z2, edges, thickness=edge_thickness)
    edges = makeLine(x1, y1, z2, x1, y2, z2, edges, thickness=edge_thickness)
    """ 3rd face """
    edges = makeLine(x2, y1, z1, x2, y2, z1, edges, thickness=edge_thickness)
    edges = makeLine(x2, y2, z1, x2, y2, z2, edges, thickness=edge_thickness)
    edges = makeLine(x2, y1, z2, x2, y2, z2, edges, thickness=edge_thickness)
    """ 4th face """
    edges = makeLine(x1, y2, z1, x1, y2, z2, edges, thickness=edge_thickness)
    edges = makeLine(x1, y2, z2, x2, y2, z2, edges, thickness=edge_thickness)
    edges = makeLine(x2, y2, z1, x2, y2, z2, edges, thickness=edge_thickness)
    edges = makeLine(x1, y2, z1, x2, y2, z1, edges, thickness=edge_thickness)


    nodes = edges.create()


    NodePath(nodes).reparentTo(render)

    faces.addGeom(square0)
    faces.addGeom(square1)
    faces.addGeom(square2)
    faces.addGeom(square3)
    faces.addGeom(square4)
    faces.addGeom(square5)

    cube = render.attachNewNode(faces)
    cube.setTwoSided(True)



def logRender(render):
    print(render.getChildren())