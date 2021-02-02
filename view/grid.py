from panda3d.core import LineSegs, NodePath, GeomVertexFormat, \
    GeomVertexData, Geom, GeomVertexWriter, GeomTriangles, GeomNode


# Class to draw a simple grid
class Grid:
    def __init__(self, showbase):
        self.render = showbase.render
        self.drawGrid()

    def drawGrid(self,x_lines=100, y_lines=100, spacing=1):
        ls = LineSegs()
        ls.setThickness(1)
        ls.setColor(0.1, 0.1, 0.1, 0.1)
        for i in range(0, x_lines):
            ls.moveTo(0, i * spacing, 0)
            ls.drawTo(100, i * spacing, 0)
            node = ls.create()
            NodePath(node).reparentTo(self.render)
        for i in range(0, y_lines):
            ls.moveTo(i * spacing, 0, 0)
            ls.drawTo(i * spacing, 100, 0)
            node = ls.create()
            NodePath(node).reparentTo(self.render)
        plane = GeomNode('plane')
        plane.addGeom(self.draw_plane())
        cube = self.render.attachNewNode(plane)

    def draw_plane(self,x1=0,y1=0,z1=0,x2=100,y2=100,z2=-0.5):
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('square', format, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')

        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        color.addData4f(0.15, 0.15, 0.15, 1.0)

        tris = GeomTriangles(Geom.UHDynamic)
        tris.addVertices(0, 1, 3)
        tris.addVertices(1, 2, 3)
        square = Geom(vdata)
        square.addPrimitive(tris)
        return square