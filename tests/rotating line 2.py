import math

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #disable mouse, we need the left click working
        base.disableMouse()
        #set sensible view
        base.cam.set_pos(20, -20, 20)
        base.cam.look_at(0,0,0)
        #help info
        self.inst1 = addInstructions(0.06, "MOUSE-1: click and hold")
        self.inst2 = addInstructions(0.12, "X, Y, Z: change rotation axis")
        self.inst3 = addInstructions(0.18, "Vector")
        self.inst4 = addInstructions(0.24, "Last vector")
        self.inst5 = addInstructions(0.30, "Position")
        #origin
        self.origin = Point3(0,0,0)
        #visual aid
        self.circle=self.make_circle()
        self.circle.hide()
        #mouse left or right click control
        self.mouse_left_is_down = False
        self.mouse_right_is_down = False

        self.last_line = None
        #a line showing the current rotation axis
        self.line=None
        #the axis node, we rotate around this node
        self.axis=render.attach_new_node('axis')
        #list of current axis, overkill here, but used for moving
        #when there are 2 movement axis(not in demo
        self.active_axis=[]
        self.toggle_axis('x')

        self.mouse_is_down=False


        #bind keys
        self.accept('mouse1', self.on_mouse_left_down)
        self.accept('mouse1-up', self.on_mouse_left_up)
        self.accept('mouse3', self.on_mouse_right_down)
        self.accept('mouse3-up', self.on_mouse_right_up)

        self.accept('mouse3', self.on_mouse_down)
        self.accept('mouse3-up', self.on_mouse_up)
        self.accept('x', self.toggle_axis, ['x'])
        self.accept('y', self.toggle_axis, ['y'])
        self.accept('z', self.toggle_axis, ['z'])
        #run task
        taskMgr.add(self.mouse_task, 'mouse_tsk')

        #Add card
        c = CardMaker('DrawingPlane')
        color = (0.15, 0.15, 0.15, 1)
        c.setFrameFullscreenQuad()
        c.setColor(color)
        """ Attach to render and rotate the card """
        card = c.generate()
        self.render.attachNewNode(card).lookAt(0, 0, -1)

    def make_circle(self, segments = 360, thickness=2.0, radius=1.0):
        l=LineSegs()
        l.set_thickness(thickness)
        l.move_to(self.origin)
        l.draw_to((0, radius, 0))
        temp = NodePath('temp')
        for i in range(segments + 1):
            temp.set_h(i * 360.0 / segments)
            p = render.get_relative_point(temp, (0, radius/2, 0))
            l.draw_to(p)
        temp.remove_node()
        return render.attach_new_node(l.create())

    def on_mouse_left_down(self):
        self.mouse_left_is_down = True
        print('mouse left down')

    def on_mouse_right_down(self):
        self.mouse_right_is_down = True
        print('mouse right down')

    def on_mouse_left_up(self):
        self.mouse_left_is_down = False
        self.origin = Point3(0,0,0)
        print('mouse left up')

    def on_mouse_right_up(self):
        self.mouse_right_is_down = False
        print('mouse right up')


    def on_mouse_down(self):
        self.last_vec=None
        self.last_hpr=None
        self.mouse_is_down=True

    def on_mouse_up(self):
        self.mouse_is_down=False
        self.inst4.setText(str(self.last_vec))

        l = LineSegs()
        l.move_to(Point3(0, 0, 0))
        l.draw_to((self.last_line.x, self.last_line.y, self.last_line.z))
        render.attach_new_node(l.create())

        self.circle.hide()

    def toggle_axis(self, axis):
        if axis in self.active_axis:
            self.active_axis.pop(self.active_axis.index(axis))
        else:
            self.active_axis.append(axis)
        while len(self.active_axis)>1:
            axis=self.active_axis[0]
            self.toggle_axis(axis)
        self.update_axis(Point3(0,0,0))

    def update_axis(self, point):
        '''Creates a plane to capture mouse clicks,
        the pos of self.axis defines the point for the plane,
        the normal of the plane depends on what is
        the current axis in self.active_axis.
        Also draws a line/vector to show the axis.
        '''
        #self.axis.set_pos(Point3(0,0,0))
        #point=self.axis.get_pos(render)
        if 'x' in self.active_axis:
            vec=self.axis.get_quat().get_right()
        elif 'y' in self.active_axis:
            vec=self.axis.get_quat().get_forward()
        elif 'z' in self.active_axis:
           vec=self.axis.get_quat().get_up()
        #remove old line
        if self.line:
            self.line.remove_node()
        #draw new line
        if self.active_axis:
            self.plane=Plane(vec, point)#also make the plane, kind of important...
            l=LineSegs()
            l.set_thickness(2.0)
            l.move_to(point)
            l.draw_to((point+vec))
            self.line=render.attach_new_node(l.create())
            self.line.set_color((abs(vec.x), abs(vec.y), abs(vec.z), 1.0), 1)
            self.circle.set_color(self.line.get_color(), 1) #recolor the circle to make it fit

    def mouse_task(self, task):
        '''Rotates self.model around self.axis based on mouse movement '''
        if self.mouse_is_down and self.active_axis:
            if base.mouseWatcherNode.has_mouse():
                # get the mouse ray-plane intersection
                # kudos to rdb
                mpos = base.mouseWatcherNode.get_mouse()
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
                    # make a direction vector
                    #vec = self.axis.get_pos() - pos3d
                    # visual aid
                    #self.circle.set_scale(vec.length())
                    # make a direction vector
                    vec = pos3d - self.axis.get_pos()
                    # calculate the angle
                    angle = 0
                    if self.active_axis[0] == 'x':
                        angle = math.atan2(vec.y, vec.z)
                    if self.active_axis[0] == 'y':
                        angle = math.atan2(vec.x, vec.z)
                    if self.active_axis[0] == 'z':
                        angle = math.atan2(vec.x, vec.y)

                    angle_in_degrees = round(math.degrees(angle))
                    if angle_in_degrees % 5 == 0:
                        if angle_in_degrees < 0:
                            angle_in_degrees += 360
                        self.inst3.setText(str(angle_in_degrees))
                        # visual aid
                        self.circle.set_scale(vec.length())
                        self.circle.look_at(pos3d, self.plane.get_normal())
                        #improvement
                        self.circle.set_pos(self.origin)
                        self.circle.show()
                        self.last_line = LVecBase3f(vec.x,vec.y,vec.z)



                    # we just need the direction
                    vec.normalize()



                    # nothing more to do at this point if we have no stored vector
                    if self.last_vec is None:
                        self.last_vec = vec
                        return task.again

                    self.last_vec = vec
        return task.again


app = MyApp()
app.run()