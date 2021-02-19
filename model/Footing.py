from model.StructuralElement import StructuralElement


class Footing(StructuralElement):
    """Class to define a footing"""
    def __init__(self,x,y):
        """Initializer

        :param x: The center X position
        :type x: float
        :param y: The center Y position
        :type y: float
        """
        self.x = x
        self.y = y


class ShallowFooting(Footing):
    """Class to define a shallow footing"""
    def __init__(self,A,B,a,b,z):
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
        """
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.z = z

