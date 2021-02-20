from panda3d.core import LineSegs, NodePath,CardMaker, GeomNode

from view.Geometry import makeLine


class Grid:
    """
    Class to draw a simple grid in the scene,
    this class also has a method to draw a plane to serve as reference to drawing
    """
    def __init__(self, showbase):
        """
        Constructor method
        """
        self.render = showbase.render
        self.draw_grid()
        self.draw_plane()

    def draw_grid(self, lines=100, spacing=1.0, thickness=1, color = (0.1, 0.1, 0.1, 0.1), z_shift=0.05):
        """Method to draw a simple finite grid in the scene

        :param lines: Number of lines
        :type lines: int
        :param spacing: Grid spacing=1
        :type spacing: float
        :param thickness: Line's thickness
        :type thickness: int
        :param color: Line's color
        :type color: tuple
        :param z_shift: Displacement of grid in relation to xy plane
        :type z_shift: float
        """
        ls = LineSegs('Grid')
        ls.setThickness(thickness)
        ls.setColor(color)

        for i in range(0,lines):
            """ X line drawing """
            ls = makeLine(0, i*spacing, z_shift, lines, i*spacing, z_shift, ls)
            """ Y line drawing """
            ls = makeLine(i * spacing, 0, z_shift, i * spacing, lines, z_shift, ls)

        node = ls.create()
        NodePath(node).reparentTo(self.render)

    def draw_plane(self,a=(0,0),b=(100,100),color=(0.15,0.15,0.15,1)):
        """ Method to draw a plane using :class:`panda3d.core.CardMaker`

        :param a: The card's initial point
        :type a: tuple
        :param b: The card's final point
        :type b: tuple
        :param color: The card's color
        :type color: tuple
        """

        c = CardMaker('DrawingPlane')
        c.setFrame(a[0],b[0],a[1],b[1])
        c.setColor(color)
        """ Attach to render and rotate the card """
        self.render.attachNewNode(c.generate()).lookAt(0, 0, -1)
