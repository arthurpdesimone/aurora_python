from QPanda3D.Panda3DWorld import Panda3DWorld
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
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
        base.accept('mouse2',self.printHello)
        self.accept('escape', lambda: sys.exit())

    def printHello(self):
        self.camera.setPos(2, -50, 2)

