from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Plane, Vec3, Point3, NodePath, TextNode, LineSegs


class Color3D:
    Black = (0, 0, 0, 1)
    Gray = (0.5, 0.5, 0.5, 1)
    White = (1, 1, 1, 1)
    Red = (1, 0, 0, 1)
    Green = (0, 1, 0, 1)
    Blue = (0, 0, 1, 1)
    Yellow = (1, 1, 0, 1)


def create_axes_cross(name, size, has_labels):
    def create_axis_line(label, color, draw_to):
        coords.setColor(color)
        coords.moveTo(0, 0, 0)
        coords.drawTo(draw_to)

        # Put the axis' name in the tip
        if label != "":
            text = TextNode(label)
            text.setText(label)
            text.setTextColor(color)
            axis_np = coords_np.attachNewNode(text)
        else:
            axis_np = coords_np.attachNewNode("")
        axis_np.setPos(draw_to)
        return axis_np

    coords_np = NodePath(name)
    coords = LineSegs()
    coords.setThickness(2)
    axis_x_np = create_axis_line("X" if has_labels else "", Color3D.Red, (size, 0, 0))
    axis_y_np = create_axis_line("Y" if has_labels else "", Color3D.Green, (0, size, 0))
    axis_z_np = create_axis_line("Z" if has_labels else "", Color3D.Blue, (0, 0, size))
    node = coords.create(True)
    coords_np.attachNewNode(node)
    return coords_np, axis_x_np, axis_y_np, axis_z_np



class Distance:
    """
    Class to calculate the distance between the cursor and a plane initially set to zero height (z=0)
    """
    def __init__(self, showbase, UCS, window):
        self.window = window
        self.showbase = showbase
        z = 0
        self.plane = Plane(Vec3(0, 0, 1), Point3(0, 0, z))
        self.model = UCS.draw_cross(0, 0)
        self.model.reparentTo(render)
        self.position = Point3()
        taskMgr.add(self.get_mouse_pos, "_Distance__get_mouse_pos")

        # origin = [-2, 5, -1.0]
        # coords_np, axis_x_np, axis_y_np, axis_z_np = create_axes_cross("coords", 3, True)
        # coords_np.reparentTo(self.showbase.cam)
        # coords_np.setPos(self.showbase.cam, tuple(origin))
        # coords_np.setScale(0.1)


    def get_mouse_pos(self, task):
        """
        Method to calculate the intersection between the camera point and
        a plane specified. Also responsible for placing the UCS cursor following the mouse
        """

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
                status3d = '[' + str(pos3d.x) + ',' + str(pos3d.y) + ',' + str(pos3d.z)+ ']'
                self.window.update_statusbar(status3d)
                self.model.setPos(render, pos3d)
                self.position = pos3d
        return task.again
