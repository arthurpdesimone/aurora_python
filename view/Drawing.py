import math

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import LineSegs, NodePath, Point3, Plane, TextNode


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class Drawing():
    def __init__(self, world):
        self.showbase = world.showbase
        self.showbase.accept("line",self.command_line)
        self.inst1 = addInstructions(0.06, "MOUSE-LEFT: click and hold / MOUSE RIGHT : Draw line")
        self.inst2 = addInstructions(0.12, "X, Y, Z: change rotation axis")
        self.inst3 = addInstructions(0.18, "Vector")
        self.inst4 = addInstructions(0.24, "Last vector")
        self.inst5 = addInstructions(0.30, "Position")

        self.origin = Point3(0, 0, 0)
        # visual aid
        self.circle = self.make_circle()
        """ Mouse buttons control """
        self.mouse_left_is_down = False
        self.mouse_right_is_down = False
        # temporary line between the mouse and the origin
        self.aux_line = None
        # the line you want to draw
        self.last_line = None
        # a line showing the current rotation axis
        self.line = None
        # the axis node, we rotate around this node
        self.axis = render.attach_new_node('axis')
        # list of current axis, overkill here, but used for moving
        self.active_axis = 'z'
        self.update_axis(Point3(0, 0, 0))
        self.mouse_is_down = False

        # bind keys
        self.showbase.accept('mouse1', self.on_mouse_left_down)
        self.showbase.accept('mouse1-up', self.on_mouse_left_up)
        self.showbase.accept('mouse3', self.on_mouse_right_down)
        self.showbase.accept('mouse3-up', self.on_mouse_right_up)
        self.showbase.accept('x', self.toggle_axis, ['x'])
        self.showbase.accept('y', self.toggle_axis, ['y'])
        self.showbase.accept('z', self.toggle_axis, ['z'])
        # run task
        taskMgr.add(self.mouse_task, 'mouse_tsk')

    def draw_node(self, position):
        sphere = loader.loadModel("misc/sphere.egg")
        sphere.reparentTo(render)
        sphere.setScale(0.1)
        sphere.setPos(position)
        sphere.setColor(0, 0, 0)
        return sphere

    def on_mouse_left_down(self):
        self.mouse_left_is_down = True
        print('mouse left down')

    def on_mouse_right_down(self):
        self.mouse_right_is_down = True
        print('mouse right down')
        self.last_vec = None
        self.mouse_is_down = True

    def on_mouse_left_up(self):
        self.mouse_left_is_down = False
        print('mouse left up')

    def on_mouse_right_up(self):
        self.mouse_right_is_down = False
        print('mouse right up')
        self.inst4.setText(str(self.last_vec))

        l = LineSegs()
        self.draw_node(self.last_line[0])
        l.move_to(self.last_line[0])
        self.draw_node(self.last_line[1])
        l.draw_to(self.last_line[1])
        render.attach_new_node(l.create())

    def toggle_axis(self, axis):
        self.active_axis = axis
        self.update_axis(self.origin)

    def update_axis(self, point):
        '''Creates a plane to capture mouse clicks,
        the pos of self.axis defines the point for the plane,
        the normal of the plane depends on what is
        the current axis in self.active_axis.
        Also draws a line/vector to show the axis.
        '''
        if 'x' in self.active_axis:
            vec = self.axis.get_quat().get_right()
            self.circle.setHpr(0, 0, 90)
        elif 'y' in self.active_axis:
            vec = self.axis.get_quat().get_forward()
            self.circle.setHpr(0, 90, 0)
        elif 'z' in self.active_axis:
            vec = self.axis.get_quat().get_up()
            self.circle.setHpr(90, 0, 0)
        # remove old line
        if self.line:
            self.line.remove_node()
        # draw new line
        if self.active_axis:
            self.plane = Plane(vec, point)  # also make the plane, kind of important...
            l = LineSegs()
            l.set_thickness(2.0)
            l.move_to(point)
            l.draw_to((point + vec))
            self.line = render.attach_new_node(l.create())
            self.line.set_color((abs(vec.x), abs(vec.y), abs(vec.z), 1.0), 1)
            self.circle.set_color(self.line.get_color(), 1)  # recolor the circle to make it fit

    def mouse_task(self, task):
        '''Rotates self.model around self.axis based on mouse movement '''
        if self.active_axis:
            if base.mouseWatcherNode.hasMouse():
                # get the mouse ray-plane intersection
                mpos = base.mouseWatcherNode.getMouse()
                pos3d = Point3()
                near_point = Point3()
                far_point = Point3()
                base.camLens.extrude(mpos, near_point, far_point)
                if self.plane.intersects_line(pos3d,
                                              render.get_relative_point(base.cam, near_point),
                                              render.get_relative_point(base.cam, far_point)):

                    self.inst5.setText(str(pos3d))
                    if self.mouse_left_is_down:
                        self.update_axis(pos3d)
                        self.origin = pos3d
                        self.circle.set_pos(self.origin)

                    vec = pos3d - self.axis.get_pos()
                    angle_vector = pos3d - self.origin
                    # calculate the angle
                    angle = 0
                    if self.active_axis == 'x':
                        angle = math.atan2(angle_vector.y, angle_vector.z)
                    if self.active_axis == 'y':
                        angle = math.atan2(angle_vector.x, angle_vector.z)
                    if self.active_axis == 'z':
                        angle = math.atan2(angle_vector.x, angle_vector.y)

                    angle_in_degrees = round(math.degrees(angle))

                    if angle_in_degrees % 5 == 0:
                        if angle_in_degrees < 0:
                            angle_in_degrees += 360

                        self.inst3.setText(str(angle_in_degrees))
                        self.inst4.setText(str(angle_vector.length()))
                        if self.active_axis == 'x' or self.active_axis == 'z' or angle_vector.length() > 0:
                            self.circle.look_at(pos3d, self.plane.get_normal())
                        elif self.active_axis == 'y' and self.mouse_left_is_down:
                            self.circle.setHpr(0, 90, 0)

                        self.circle.show()
                        # remove if exists previous auxiliar line
                        if self.aux_line: self.aux_line.removeAllGeoms()
                        # draw the auxiliar line
                        l = LineSegs()
                        l.move_to(self.circle.get_pos())
                        l.draw_to(vec)
                        # store the auxiliar line
                        self.aux_line = l.create()
                        render.attach_new_node(self.aux_line)
                        self.last_line = (self.circle.get_pos(), vec)

        return task.again

    def command_line(self):
        """Method to draw a line base on current active axis"""
        """Shutdown camera temporarily"""
        self.showbase.messenger.send("remove_camera")
        """Visual aid"""
        self.circle = self.make_circle()
        pass

    def make_circle(self, segments = 360, thickness=2.0, radius=2.0):
        l=LineSegs()
        l.set_thickness(thickness)
        l.move_to(self.origin)
        l.draw_to((0, radius, 0))
        temp = NodePath('temp')
        for i in range(segments + 1):
            temp.set_h(i * 360.0 / segments)
            p = self.showbase.render.get_relative_point(temp, (0, radius/2, 0))
            l.draw_to(p)
        temp.remove_node()
        return self.showbase.render.attach_new_node(l.create())