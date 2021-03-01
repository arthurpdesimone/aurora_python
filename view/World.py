from QPanda3D.Panda3DWorld import Panda3DWorld

import sys


class World(Panda3DWorld):
    """Class to encapsulate the app and maximize window on Windows environment"""

    def __init__(self):
        Panda3DWorld.__init__(self)
        """Store a showbase reference"""
        self.showbase = base
        """Maximizing windows"""
        self.win.setClearColorActive(True)
        """ Configuration of camera and running """
        self.camera.setPos(2, -20, 2)
        self.accept('escape', lambda: sys.exit())

