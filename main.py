# Aurora python
# Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import WindowProperties

from direct.showbase.ShowBase import ShowBase
import win32gui, win32con
from view.camera import *
from view.ucs import *
from view.grid import *
from view.menu import *
from view.direct_tooltip import *
from view.distance import *


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # To enable the camera
        self.disable_mouse()
        # Maximizing window
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        camera = CameraController(self)


from direct.gui.DirectGui import DirectSlider


def showValue():
    print(slider['value'])


slider = DirectSlider(range=(0, 100), value=0, pageSize=3, scale=0.2, command=showValue,
                      pos=(1.6, 0, -0.95))

app = App()
Menu(app)
UCS(app)
Grid(app)
distance = Distance(app)
DirectTooltip(distance).show()

# Configuring window
props = WindowProperties()
props.setTitle('Aurora Python')
app.win.requestProperties(props)
app.setBackgroundColor(0, 0, 0)
# Configuration of camera and running
app.camera.setPos(4, -10, 2)
app.run()
