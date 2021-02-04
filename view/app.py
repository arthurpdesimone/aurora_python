from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
import sys
import win32gui, win32con

class App(ShowBase):
    """Class to encapsulate the app and maximize window on Windows environment"""

    def __init__(self):
        ShowBase.__init__(self)
        """To enable the camera"""
        self.disable_mouse()
        """Maximizing windows"""
        props = WindowProperties()
        props.setTitle('Aurora Python')



        self.win.requestProperties(props)
        self.setBackgroundColor(0, 0, 0)
        """ Configuration of camera and running """
        self.camera.setPos(4, -10, 2)

        """ To maximize window under windows"""
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

        self.accept('escape', lambda: sys.exit())


