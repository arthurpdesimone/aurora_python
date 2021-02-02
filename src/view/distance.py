from direct.showbase.ShowBase import ShowBase
from panda3d.core import Plane, Vec3, Point3, CardMaker

class Distance(ShowBase):
    def __init__(self, showbase):
        self.app = showbase
        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))
        self.model = loader.loadModel("jack")
        self.model.reparentTo(render)
        taskMgr.add(self.__getMousePos, "_Distance__getMousePos")

    def __getMousePos(self, task):
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            pos3d = Point3()
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mpos, nearPoint, farPoint)
            if self.plane.intersectsLine(pos3d,
                                         render.getRelativePoint(camera, nearPoint),
                                         render.getRelativePoint(camera, farPoint)):
                print("Mouse ray intersects ground plane at ", pos3d)
                self.model.setPos(render, pos3d)
        return task.again
