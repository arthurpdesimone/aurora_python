# Aurora python
# Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import WindowProperties
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, LineSegs, TextNode
import win32gui, win32con



class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disable_mouse()
        # Apply scale and position transforms on the model.
        self.camera.setPos(4,-10,2)
        #Maximizing window
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

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
    return NodePath(node)

def test(arg):
    text_x = TextNode('x')
    #text_x.setPos(0,0,0)
    #text_x.reparentTo(app.render)

# Configuring the menu file
file_menu = DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                             initialitem=0,
                             command=test,
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
ucs = P3DCreateAxes(1)
ucs.reparentTo(app.render)


props = WindowProperties()
props.setTitle('Aurora Python')
app.win.requestProperties(props)
app.setBackgroundColor(0, 0, 0)

app.run()
