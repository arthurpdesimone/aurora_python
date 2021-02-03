"""
   Aurora python
   Aiding brazilian civil engineers to build reinforced concrete buildings

   Author: Arthur Pendragon De Simone
"""

from pandac.PandaModules import WindowProperties
"""Importing the app view"""
from view.app import *
from view.ucs import *
from view.gui import *
from view.grid import *
from view.menu import *
from view.tooltip import *
from view.distance import *


if __name__ == "__main__":
    app = App()
    Menu(app)
    Gui(app)
    UCS(app)
    Grid(app)
    distance = Distance(app)
    Tooltip(distance).show()


    # Configuring window
    props = WindowProperties()
    props.setTitle('Aurora Python')
    props.setIconFilename('img/icon.ico')
    app.win.requestProperties(props)
    app.setBackgroundColor(0, 0, 0)
    # Configuration of camera and running
    app.camera.setPos(4, -10, 2)
    app.run()