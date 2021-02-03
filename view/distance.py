from direct.showbase.ShowBase import ShowBase
from panda3d.core import Plane, Vec3, Point3, CardMaker

from view.ucs import UCS


class Distance(ShowBase):
    def __init__(self, showbase):
        self.app = showbase
        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))
        self.model = UCS(self.app).draw_cross(0, 0)
        self.model.reparentTo(render)
        self.position = Point3()
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
                # print("Mouse ray intersects ground plane at ", pos3d)
                # Round the point
                pos3d = Point3(round(pos3d.x,0),round(pos3d.y,0),round(pos3d.z,0))
                self.model.setPos(render, pos3d)
                self.position = pos3d
        return task.again
