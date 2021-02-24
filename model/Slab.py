from panda3d.core import LVecBase4f

from view.Geometry import makeCube

class Slab:
    """ Class to define a column"""
    def __init__(self, x, y, z):
        """Initializer

        :param x: The center X position
        :type x: float
        :param y: The center Y position
        :type y: float
        :param z: The center Z position
        :type z: float
        """
        self.x = x
        self.y = y
        self.z = z



class RectangularSlab(Slab):
    """ Class to define a rectangular slab """
    def __init__(self, x, y, z, t):
        """Initializer

        :param t: The slab thickness
        :type t: float
        """

        super().__init__(x, y, z)
        self.t = t

    def draw(self, render):
        """ Method to draw itself

        :param render: render
        """

        color = LVecBase4f(0.5, 0.5, 0.5, 1)
        """ Draw base """
        first_corner = (self.x -self.b / 2,self.y -self.d / 2, self.z - self.t / 2)
        last_corner = (self.x +self.b / 2,self.y +self.d / 2, self.z + self.t / 2)

        makeCube(first_corner[0], first_corner[1], first_corner[2],
                last_corner[0], last_corner[1], last_corner[2],
                render, color_face=color)