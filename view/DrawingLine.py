import math

from panda3d.core import LineSegs, NodePath, Point3, Plane

from view.tools.Log import Log


class DrawingLine():
    log = Log.instance()

    def __init__(self, world, window):
        self.window = window
        self.showbase = world.showbase
        self.showbase.accept("line",self.command_line)

    def command_line(self):
        """Method to draw a line base on current active axis"""
        """Shutdown camera temporarily"""
        self.showbase.messenger.send("remove_camera")

        self.origin = Point3(0, 0, 0)
        # visual aid
        self.circle = self.make_circle()
        """ Mouse buttons control """
        self.mouse_left_is_down = False
        self.mouse_right_is_down = False
        # temporary line between the mouse and the origin
        self.aux_line = None
        self.aux_line_node = None
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

        self.bind_keys()
        """ Escape binded function """
        self.showbase.accept('escape', self.unbind_keys)
        # run task
        taskMgr.add(self.mouse_task, 'mouse_tsk')

    def bind_keys(self):
        """Method to bind useful keys to drawing"""
        self.showbase.accept('mouse1', self.on_mouse_left_down)
        self.showbase.accept('mouse1-up', self.on_mouse_left_up)
        self.showbase.accept('mouse2', self.on_mouse_right_down)
        self.showbase.accept('mouse2-up', self.on_mouse_right_up)
        self.showbase.accept('x', self.toggle_axis, ['x'])
        self.showbase.accept('y', self.toggle_axis, ['y'])
        self.showbase.accept('z', self.toggle_axis, ['z'])

    def unbind_keys(self):
        """ Remove all key bindings """
        self.log.appendLog("Escape pressionado, desassociando criação de linhas")
        taskMgr.remove('mouse_tsk')
        self.showbase.ignore('mouse1')
        self.showbase.ignore('mouse1-up')
        self.showbase.ignore('mouse2')
        self.showbase.ignore('mouse2-up')
        self.showbase.ignore('x')
        self.showbase.ignore('y')
        self.showbase.ignore('z')

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

        l = LineSegs("Line")
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
            l = LineSegs('eixo')
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
                """Get the mouse ray-plane intersection"""
                mpos = base.mouseWatcherNode.getMouse()
                pos3d = Point3()
                near_point = Point3()
                far_point = Point3()
                base.camLens.extrude(mpos, near_point, far_point)
                """Check if mouse intersects virtual plane """
                if self.plane.intersects_line(pos3d,
                                              render.get_relative_point(base.cam, near_point),
                                              render.get_relative_point(base.cam, far_point)):

                    """If mouse left is down update axis reference"""
                    if self.mouse_left_is_down:
                        self.update_axis(pos3d)
                        self.origin = pos3d
                        self.circle.set_pos(self.origin)
                        self.window.update_statusbar(str(self.origin))

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

                        length = angle_vector.length()
                        if self.active_axis == 'x' or self.active_axis == 'z' or length > 0:
                            self.circle.look_at(pos3d, self.plane.get_normal())
                        elif self.active_axis == 'y' and self.mouse_left_is_down:
                            self.circle.setHpr(0, 90, 0)

                        self.circle.show()
                        # remove if exists previous auxiliar line
                        if self.aux_line:
                            self.aux_line.removeAllGeoms()
                            self.aux_line_node.removeNode()
                        # draw the auxiliar line
                        l = LineSegs("Auxiliary line")
                        l.move_to(self.circle.get_pos())
                        l.draw_to(vec)
                        # store the auxiliar line
                        self.aux_line = l.create()
                        self.aux_line_node = render.attach_new_node(self.aux_line)
                        self.last_line = (self.circle.get_pos(), vec)

        return task.again


    def make_circle(self, segments = 360, thickness=2.0, radius=1.0):
        """ Draw a circle to auxiliate a line drawing """
        l=LineSegs('Auxiliary circle')
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