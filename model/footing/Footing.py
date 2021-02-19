class Footing():
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
        pass


class ShallowFooting(Footing):
    """Class to define a shallow footing"""
    def __init__(self):
        pass
