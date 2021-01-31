#Aurora python
#Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import ConfigVariableBool
from pandac.PandaModules import ConfigVariableInt
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode
import win32gui, win32con
from direct.showbase.DirectObject import DirectObject   # for event handling
import direct.directbase.DirectStart
import sys

class World(DirectObject):

   def __init__(self):
        # Get window handle (Windows only).
        super().__init__()
        self.hwnd = win32gui.GetForegroundWindow()

        # Maximise window (Windows only).
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND,win32con.SC_MAXIMIZE, 0)

        #On ESC close window
        self.accept("escape",sys.exit)

w= World()

# Add some text
bk_text = "This is my Demo"
textObject = OnscreenText(text=bk_text, pos=(0.95,-0.95), scale=0.07,
                          fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                          mayChange=1)

# Callback function to set  text
def setText():
        bk_text = "Button Clicked"
        textObject.setText(bk_text)

# Add button
b = DirectButton(text=("OK", "click!", "rolling over", "disabled"),
                 scale=.1, command=setText)


base.run()