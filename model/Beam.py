import abc
from math import sqrt

from PyNite.Node3D import Node3D
from panda3d.core import LVecBase4f

from view.Geometry import makeCube

class Beam():
    """ Class to define a beam """

    def __init__(self, initial_node, end_node):
        """Initializer

        :param initial_node: The node describing the beginning of the beam
        :type initial_node: :class:'PyNite.Node3D'
        :param end_node: The node describing the end of the beam
        :type end_node: :class:'PyNite.Node3D'

        """
        self.initial_node = initial_node
        self.end_node = end_node
        self.length = self.calculate_length()
        self.draw()
        print(initial_node,end_node,self.length)


    @abc.abstractmethod
    def calculate_length(self):
        """ Calculate the length of a beam"""
        x0 = self.initial_node.X
        y0 = self.initial_node.Y
        z0 = self.initial_node.Z
        x1 = self.end_node.X
        y1 = self.end_node.Y
        z1 = self.end_node.Z
        delta_x = x1 - x0
        delta_y = y1 - y0
        delta_z = z1 - z0

        length = sqrt(pow(delta_x, 2)+pow(delta_y, 2)+pow(delta_z, 2))
        return length

    @abc.abstractmethod
    def draw(self):
        pass

# class RectangularBeam(Beam):
#     """ Class to define a beam """
#
#     def __init__(self, h, bw, x, y, z, l):
#         """Initializer
#
#         :param h: The beam height
#         :type h: float
#         :param bw: The beam width
#         :type bw: float
#         """
#         super().__init__(x, y, z, l)
#         self.h = h
#         self.bw = bw
#
#     def draw(self, render):
#         """ Method to draw itself
#
#         :param render: render
#         """
#
#         color = LVecBase4f(0.5, 0.5, 0.5, 1)
#         """ Draw base """
#         first_corner = (self.x -self.bw / 2,self.y -self.l / 2,self.z -self.h / 2)
#         last_corner = (self.x +self.bw / 2,self.y +self.l / 2,self.z +self.h / 2)
#
#         makeCube(first_corner[0],first_corner[1],first_corner[2],
#                  last_corner[0],last_corner[1],last_corner[2],
#                  render, color_face=color)

