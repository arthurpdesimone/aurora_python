
from QPanda3D.Panda3DWorld import Panda3DWorld

class World(Panda3DWorld):
    """ Class to control the whole panda 3d world
    This class contains:
    * An UCS (universal coordinate system) symbol class to orient the user
    * A grid class to draw a 100x100 grid with given line spacing
    """

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
        taskMgr.doMethodLater(5,self.get_world_children, "_World__get_world_children")

    def get_world_children(self,task):
        old = len(self.showbase.render.getChildren())
        new = len(self.temp_render_children)
        print(f'Old {old} new {new}')
        if len(self.showbase.render.getChildren()) != len(self.temp_render_children):
            print("Render mudou")
            for child in self.showbase.render.getChildren():
                print(child.getName())
        self.temp_render_children = self.showbase.render.getChildren()
        return task.again
