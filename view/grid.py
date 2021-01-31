from panda3d.core import LineSegs, NodePath


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