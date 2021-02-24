from panda3d.core import LVecBase4f

from view.Geometry import makeCube


class Beam:
    """ Class to define a beam """

    def __init__(self, x, y, z, l):
        """Initializer

        :param x: The center X position
        :type x: float
        :param y: The center Y position
        :type y: float
        :param z: The center Z position
        :type z: float
        :param l: The length of the beam
        :type l: float

        """

        self.x = x
        self.y = y
        self.z = z
        self.l = l


class RectangularBeam(Beam):
    """ Class to define a beam """

    def __init__(self, h, bw, x, y, z, l):
        """Initializer

        :param h: The beam height
        :type h: float
        :param bw: The beam width
        :type bw: float
        """
        super().__init__(x, y, z, l)
        self.h = h
        self.bw = bw

    def draw(self, render):
        """ Method to draw itself

        :param render: render
        """

        color = LVecBase4f(0.5, 0.5, 0.5, 1)
        """ Draw base """
        first_corner = (self.x -self.bw / 2,self.y -self.l / 2,self.z -self.h / 2)
        last_corner = (self.x +self.bw / 2,self.y +self.l / 2,self.z +self.h / 2)

        makeCube(first_corner[0],first_corner[1],first_corner[2],
                 last_corner[0],last_corner[1],last_corner[2],
                 render, color_face=color)

