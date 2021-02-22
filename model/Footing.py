from panda3d.core import LineSegs, NodePath

from model.Column import Column
from model.StructuralElement import StructuralElement
from view.Geometry import *


class Footing(StructuralElement):
    """Class to define a footing"""
    def __init__(self,x,y):
        """Initializer

        :param x: The center X position
        :type x: float
        :param y: The center Y position
        :type y: float
        :param column: The column that unloads at the footing
        :type column: model.Column.Column
        """
        self.x = x
        self.y = y


class ShallowFooting(Footing):
    """Class to define a shallow footing"""
    def __init__(self, A, B, a, b, z, h0, h, x, y):
        """Initializer

        :param A: The bottom measure in the y-direction
        :type A: float
        :param B: The bottom measure in the x-direction
        :type B: float
        :param a: The top measure in the y-direction
        :type a: float
        :param b: The top measure in the x-direction
        :type b: float
        :param z: The bottom of the shallow foundation
        :type z: float
        :param h0: The height of the flat part
        :type h0: float
        :param h: The total height
        :type h: float
        """
        super().__init__(x, y)
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.z = z
        self.h0 = h0
        self.h = h

        """ Lower left corner bottom inferior"""
        self.low_left_bottom_inf = [self.x - self.B / 2, self.y - self.A / 2, self.z]
        """ Lower Right corner bottom inferior"""
        self.low_right_bottom_inf = [self.x + self.B / 2, self.y - self.A / 2, self.z]
        """ Upper Left corner bottom inferior"""
        self.up_left_bottom_inf = [self.x - self.B / 2, self.y + self.A / 2, self.z]
        """ Upper Right corner bottom inferior"""
        self.up_left_bottom_inf = [self.x + self.B / 2, self.y + self.A / 2, self.z]

        """ Lower left corner bottom superior"""
        self.low_left_bottom_sup = [self.x - self.B / 2, self.y - self.A / 2, self.z+self.h0]
        """ Lower Right corner bottom superior"""
        self.low_right_bottom_sup = [self.x + self.B / 2, self.y - self.A / 2, self.z+self.h0]
        """ Upper Left corner bottom superior"""
        self.up_left_bottom_sup = [self.x - self.B / 2, self.y + self.A / 2, self.z+self.h0]
        """ Upper Right corner bottom superior"""
        self.up_right_bottom_sup = [self.x + self.B / 2, self.y + self.A / 2, self.z+self.h0]

        """ Lower left corner superior"""
        self.low_left_sup = [self.x - self.b / 2, self.y - self.a / 2, self.z + self.h]
        """ Lower Right corner superior"""
        self.low_right_sup = [self.x + self.b / 2, self.y - self.a / 2, self.z + self.h]
        """ Upper Left corner superior"""
        self.up_left_sup = [self.x - self.b / 2, self.y + self.a / 2, self.z + self.h]
        """ Upper Right corner superior"""
        self.up_right_sup = [self.x + self.b / 2, self.y + self.a / 2, self.z + self.h]

    def draw(self, render):
        """ Method to draw itself

        :param render: render
        """
        color = LVecBase4f(0.5,0.5,0.5,1)

        """ Draw base """
        makeCube(self.low_left_bottom_inf[0], self.low_left_bottom_inf[1], self.low_left_bottom_inf[2],
                 self.up_right_bottom_sup[0], self.up_right_bottom_sup[1],self.up_right_bottom_sup[2],
                 render, color_face=color)
        """ Front slope """
        front_slope = [(self.low_left_bottom_sup[0],self.low_left_bottom_sup[1],self.low_left_bottom_sup[2]),
                       (self.low_right_bottom_sup[0],self.low_right_bottom_sup[1],self.low_right_bottom_sup[2]),
                       (self.low_right_sup[0],self.low_right_sup[1],self.low_right_sup[2]),
                       (self.low_left_sup[0],self.low_left_sup[1],self.low_left_sup[2])]
        makePolygon(front_slope, render, color_face=color)
        """ Back slope """
        back_slope = [(self.up_left_bottom_sup[0], self.up_left_bottom_sup[1], self.up_left_bottom_sup[2]),
                       (self.up_right_bottom_sup[0], self.up_right_bottom_sup[1], self.up_right_bottom_sup[2]),
                       (self.up_right_sup[0], self.up_right_sup[1], self.up_right_sup[2]),
                       (self.up_left_sup[0], self.up_left_sup[1], self.up_left_sup[2])]
        makePolygon(back_slope, render, color_face=color)
        """ Left slope """
        left_slope = [(self.low_left_bottom_sup[0], self.low_left_bottom_sup[1], self.low_left_bottom_sup[2]),
                      (self.low_left_sup[0], self.low_left_sup[1], self.low_left_sup[2]),
                      (self.up_left_sup[0], self.up_left_sup[1], self.up_left_sup[2]),
                      (self.up_left_bottom_sup[0], self.up_left_bottom_sup[1], self.up_left_bottom_sup[2])]
        makePolygon(left_slope, render, color_face=color)
        """ Right slope """
        right_slope = [(self.low_right_bottom_sup[0], self.low_right_bottom_sup[1], self.low_right_bottom_sup[2]),
                      (self.low_right_sup[0], self.low_right_sup[1], self.low_right_sup[2]),
                      (self.up_right_sup[0], self.up_right_sup[1], self.up_right_sup[2]),
                      (self.up_right_bottom_sup[0], self.up_right_bottom_sup[1], self.up_right_bottom_sup[2])]
        makePolygon(right_slope, render, color_face=color)

        """ Draw top"""
        square = makeSquare(self.low_left_sup[0],self.low_left_sup[1],self.low_left_sup[2],
                   self.up_right_sup[0],self.up_right_sup[1],self.up_right_sup[2],
                   color_square=color)

        top_face = GeomNode('Face')
        top_face.addGeom(square)
        top = render.attachNewNode(top_face)
        top.setTwoSided(True)

        pass
