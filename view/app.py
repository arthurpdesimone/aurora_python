from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
import sys

class App(ShowBase):
    """Class to encapsulate the app and maximize window on Windows environment"""

    def __init__(self):
        ShowBase.__init__(self)
        """To enable the camera"""
        self.disable_mouse()
        """Maximizing windows"""
        props = WindowProperties()
        props.set_size(1366, 768)
        props.setFullscreen(True)
        props.setTitle('Aurora Python')
        self.win.requestProperties(props)
        self.setBackgroundColor(0, 0, 0)
        """ Configuration of camera and running """
        self.camera.setPos(4, -10, 2)
        self.accept('escape', lambda: sys.exit())


