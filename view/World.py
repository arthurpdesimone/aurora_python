from QPanda3D.Panda3DWorld import Panda3DWorld


class World(Panda3DWorld):
    """ Class to control the whole panda 3d world
    This class contains:
    * An UCS (universal coordinate system) symbol class to orient the user
    * A grid class to draw a 100x100 grid with given line spacing
    """

    def __init__(self):
        Panda3DWorld.__init__(self)
        """Store a showbase reference"""
        self.showbase = base
        """Maximizing windows"""
        self.win.setClearColorActive(True)
        """ Configuration of camera and running """
        self.camera.setPos(2, -10, 2)
