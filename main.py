# Aurora python
# Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import WindowProperties

import win32gui, win32con
from src.view.camera import *
from src.view.ucs import *
from src.view.grid import *
from src.view.menu import *
from src.view.distance import *
from src.view.direct_tooltip import *

"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""


class App(ShowBase):
    """
    App's main class, it initialize on Windows and maximize the window
    """
    def __init__(self):
        """Docstring for A."""
        ShowBase.__init__(self)
        # To enable the camera
        self.disable_mouse()
        # Maximizing window
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)




app = App()
Menu(app)
CameraController(app)
UCS(app)
Grid(app)
Distance(app)

tt = DirectTooltip()
tt.show("my test message")

# Configuring window
props = WindowProperties()
props.setTitle('Aurora Python')
app.win.requestProperties(props)
app.setBackgroundColor(0, 0, 0)
# Configuration of camera and running
app.camera.setPos(4, -10, 2)
#app.run()
