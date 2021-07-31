
from QPanda3D.Panda3DWorld import Panda3DWorld

from lang.Language import RENDER_CHANGED
from view.tools.Log import Log


class World(Panda3DWorld):
    """ Class to control the whole panda 3d world
    This class contains:
    * An UCS (universal coordinate system) symbol class to orient the user
    * A grid class to draw a 100x100 grid with given line spacing
    """
    log = Log.instance()

    def __init__(self):
        Panda3DWorld.__init__(self)
        """Store a showbase reference"""
        self.showbase = base
        """Maximizing windows"""
        self.win.setClearColorActive(True)
        """ Configuration of camera and running """
        self.camera.setPos(2, -10, 2)
        """ Saving children """
        self.children = self.showbase.render.getChildren()
        """ Temporary children """
        self.temp_render_children = list()
        taskMgr.doMethodLater(1,self.get_world_children, "_World__get_world_children")

    def get_world_children(self,task):
        old = len(self.showbase.render.getChildren())
        new = len(self.temp_render_children)
        print(f'Old {old} new {new}')
        #print(self.messenger.detailed_repr())
        if old != new:
            self.log.appendLog(RENDER_CHANGED)
            self.messenger.send("children_change")
        self.temp_render_children = self.showbase.render.getChildren()
        return task.again
