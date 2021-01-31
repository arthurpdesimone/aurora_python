# Aurora python
# Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import WindowProperties
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, LineSegs
import win32gui, win32con
from direct.showbase.DirectObject import DirectObject  # for event handling
import sys



class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Apply scale and position transforms on the model.
        self.camera.setPos(0,0,10)

app = App()

def P3DCreateAxes(lineThickness=1):
    ls = LineSegs()
    ls.setThickness(lineThickness)

    # X axis
    ls.setColor(1.0, 0.0, 0.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(1.0, 0.0, 0.0)

    # Y axis
    ls.setColor(0.0, 1.0, 0.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(0.0, 1.0, 0.0)

    # Z axis
    ls.setColor(0.0, 0.0, 1.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(0.0, 0.0, 1.0)

    node = ls.create()
    app.render.attachNewNode(node)
    return NodePath(node)



class World(DirectObject):

    def __init__(self):
        # Get window handle (Windows only).
        super().__init__()
        self.hwnd = win32gui.GetForegroundWindow()

        # Maximise window (Windows only).
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

        # On ESC close window
        self.accept("escape", sys.exit)


# Configuring the menu file
file_menu = DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                             initialitem=0,
                             scale=.05,
                             textMayChange=0,
                             pos=(-0.96, 0, 0.96))

# Configuring the menu architecture
arq_menu = DirectOptionMenu(items=['Arquitetura', 'Laje', 'Viga', 'Pilar', 'Fundação'],
                            initialitem=0,
                            scale=.05,
                            textMayChange=0,
                            pos=(-0.74, 0, 0.96))



# Configuring window
w = World()
ucs = P3DCreateAxes(1)
ucs.reparentTo(app.render)


props = WindowProperties()
props.setTitle('Aurora Python')
app.win.requestProperties(props)
app.setBackgroundColor(0, 0, 0)

app.run()
