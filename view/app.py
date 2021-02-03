from direct.showbase.ShowBase import ShowBase
import win32gui, win32con
from view.camera import *


class App(ShowBase):
    """Class to encapsulate the app and maximize window on Windows environment"""

    def __init__(self):
        ShowBase.__init__(self)
        """To enable the camera"""
        self.disable_mouse()
        """Maximizing windows"""
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        CameraController(self)
