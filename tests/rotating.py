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
        self.inst1 = addInstructions(0.06, "MOUSE-1: click and hold to rotate teapot")
        self.inst2 = addInstructions(0.12, "X, Y, Z: change rotation axis")
        self.inst3 = addInstructions(0.18, "R: reset rotation to (0,0,0)")

        #add some light
        ambient = AmbientLight('ambient')
        ambient.set_color((.55, .55, .65, 1))
        directional = DirectionalLight("directional")
        directional.set_direction(LVector3(0, 0.25, -1))
        directional.set_color((0.5, 0.5, 0.35, 1))
        render.set_light(render.attach_new_node(ambient))
        render.set_light(render.attach_new_node(directional))

        #visual aid
        self.circle=self.make_circle()
        self.circle.hide()
        self.circle.set_light_off()

        #the model we will rotate
        self.model=loader.load_model('teapot')
        self.model.reparent_to(render)
        #a line showing the current rotation axis
        self.line=None
        #the axis node, we rotate around this node
        self.axis=render.attach_new_node('axis')
        #list of current axis, overkill here, but used for moving
        #when there are 2 movement axis(not in demo
        self.active_axis=[]
        self.toggle_axis('z')

        self.mouse_is_down=False

        #bind keys
        self.accept('mouse1', self.on_mouse_down)
        self.accept('mouse1-up', self.on_mouse_up)
        self.accept('x', self.toggle_axis, ['x'])
        self.accept('y', self.toggle_axis, ['y'])
        self.accept('z', self.toggle_axis, ['z'])
        self.accept('r', self.reset)
        #run task
        taskMgr.add(self.mouse_task, 'mouse_tsk')

    def make_circle(self, segments=36, thickness=2.0, radius=1.0, line=True):
        l=LineSegs()
        l.set_thickness(thickness)
        l.move_to(Point3(0,0,0))
        if line:
            l.draw_to(Point3(0,radius,0))
        else:
            l.move_to(Point3(0,radius,0))
        temp=NodePath('temp')
        for i in range(segments+1):
            temp.set_h(i*360.0/segments)
            p=render.get_relative_point(temp, (0, radius, 0))
            l.draw_to(p)
        temp.remove_node()
        return render.attach_new_node(l.create())

    def on_mouse_down(self):
        self.last_vec=None
        self.last_hpr=None
        self.mouse_is_down=True

    def on_mouse_up(self):
        self.mouse_is_down=False
        self.circle.hide()
        #uncomment this line to fix all problems...and loose the rotation permanently
        #self.model.flatten_light()

    def reset(self):
        self.model.set_hpr(render, Vec3(0,0,0))

    def toggle_axis(self, axis):
        if axis in self.active_axis:
            self.active_axis.pop(self.active_axis.index(axis))
        else:
            self.active_axis.append(axis)
        while len(self.active_axis)>1:
            axis=self.active_axis[0]
            self.toggle_axis(axis)
        self.update_axis()

    def update_axis(self):
        '''Creates a plane to capture mouse clicks,
        the pos of self.axis defines the point for the plane,
        the normal of the plane depends on what is
        the current axis in self.active_axis.
        Also draws a line/vector to show the axis.
        '''
        self.axis.set_pos(self.model.get_pos())
        point=self.axis.get_pos(render)
        if 'x' in self.active_axis:
            vec=self.axis.get_quat().get_right()*-1.0
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
            l.draw_to(vec*10.0)
            self.line=render.attach_new_node(l.create())
            self.line.set_color((abs(vec.x), abs(vec.y), abs(vec.z), 1.0), 1)
            self.circle.set_color(self.line.get_color(), 1) #recolor the circle to make it fit

    def mouse_task(self, task):
        '''Rotates self.model around self.axis based on mouse movement '''
        if self.mouse_is_down and self.active_axis:
            if base.mouseWatcherNode.has_mouse():
                #get the mouse ray-plane intersection
                #kudos to rdb
                mpos = base.mouseWatcherNode.get_mouse()
                pos3d = Point3()
                near_point = Point3()
                far_point = Point3()
                base.camLens.extrude(mpos, near_point, far_point)
                if self.plane.intersects_line(pos3d,
                                              render.get_relative_point(base.cam, near_point),
                                              render.get_relative_point(base.cam, far_point)):

                    #make a direction vector
                    vec=self.axis.get_pos()-pos3d
                    #visual aid
                    self.circle.set_scale(vec.length())
                    self.circle.heads_up(pos3d, self.plane.get_normal())
                    self.circle.show()
                    #we just need the direction
                    vec.normalize()
                    #nothing more to do at this point if we have no stored vector
                    if self.last_vec is None:
                        self.last_vec=vec
                        return task.again
                    #get an angle between the vec and the vec from last frame
                    angle=vec.signed_angle_deg(self.last_vec, self.plane.get_normal())#how do I actually use this func?
                    q=Quat()
                    q.set_from_axis_angle(angle, self.plane.get_normal())
                    #can we add quats? - apparently not like this
                    #self.model.set_quat(self.axis, self.model.get_quat(self.axis)-q)
                    #this is probably wrong as well...
                    self.model.set_hpr(self.axis, self.model.get_hpr(self.axis)-q.get_hpr())
                    #print some debug)
                    #print(self.model.get_hpr(render))
                    #store the vec for next frame
                    self.last_vec=vec
        return task.again

app = MyApp()
app.run()