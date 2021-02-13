from direct.showbase.ShowBase import ShowBase
from panda3d.core import Plane, Vec3, Point3

from view.UCS import UCS
class Distance(ShowBase):
    """
    Class to calculate the distance between the cursor and a plane initially set to zero height (z=0)
    """
    def __init__(self, showbase, UCS):
        self.app = showbase
        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))
        self.model = UCS.draw_cross(0, 0)
        self.model.reparentTo(render)
        self.position = Point3()
        taskMgr.add(self.get_mouse_pos, "_Distance__get_mouse_pos")


    def get_mouse_pos(self, task):
        """
        Method to calculate the intersection between the camera point and
        a plane specified. Also responsible for placing the UCS cursor following the mouse
        """
        #.. math::
        #    (a + b)^2 = a^2 + 2ab + b^2

        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            pos3d = Point3()
            nearPoint = Point3()
            farPoint = Point3()
            base.camLens.extrude(mpos, nearPoint, farPoint)
            relativeNearPoint = render.getRelativePoint(camera, nearPoint)
            relativeFarPoint = render.getRelativePoint(camera, farPoint)

            if self.plane.intersectsLine(pos3d,relativeNearPoint,relativeFarPoint):
                # Round the point
                pos3d = Point3(round(pos3d.x,0),round(pos3d.y,0),round(pos3d.z,0))
                self.model.setPos(render, pos3d)
                self.position = pos3d
        return task.again
