from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
import sys


class App(ShowBase):
    """Class to encapsulate the app and maximize window on Windows environment"""

    def __init__(self):
        ShowBase.__init__(self)
        self.base = base
        """To enable the camera"""
        self.disable_mouse()
        """Maximizing windows"""
        props = WindowProperties()
        props.setTitle('Aurora Python')
        self.setBackgroundColor(0, 0, 0)

        """ Configuration of camera and running """
        self.camera.setPos(2, -20, 2)

        """ To maximize window under windows"""
        xSize = base.pipe.getDisplayWidth()
        ySize = base.pipe.getDisplayHeight()
        props = WindowProperties()
        props.setSize(xSize, ySize)
        props.setFixedSize(1)
        self.win.requestProperties(props)

        self.accept('escape', lambda: sys.exit())


