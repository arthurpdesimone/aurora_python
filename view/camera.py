from direct.showbase.DirectObject import DirectObject
from panda3d.core import Point3, Point2, Vec3, Plane


class CameraController:
    """
    Class to control camera using mouse
    """

    def __init__(self, showbase):
        """
        Constructor and variable initializing
        """
        self.showbase = showbase
        self.task_mgr = showbase.task_mgr
        self.world = showbase.render
        self.cam = showbase.camera
        self.mouse_watcher = showbase.mouseWatcherNode
        self.cam_lens = showbase.camLens
        self.cam_target = showbase.render.attach_new_node("camera_target")
        self.cam.reparent_to(self.cam_target)
        self.cam.set_y(-10.)
        self.mouse_prev = Point2()
        win_props = showbase.win.get_properties()
        w, h = win_props.get_x_size(), win_props.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        self.pan_start_pos = Point3()
        self.listener = DirectObject()
        self.listener.accept_once("mouse1", self.start_orbiting)
        self.listener.accept_once("mouse2", self.start_panning)
        self.set_zoom_listener()

    def set_zoom_listener(self):
        """
        Method to attach the mouse wheel to
        :meth:`~camera.CameraController.zoom_step_in` and
        :meth:`~camera.CameraController.zoom_step_out`
        """
        self.listener.accept("wheel_up", self.zoom_step_in)
        self.listener.accept("wheel_down", self.zoom_step_out)

    def stop_navigating(self):
        """
        Method to stop orbiting and start to accept other mouse inputs
        """
        self.task_mgr.remove("transform_cam")
        self.listener.accept_once("mouse1", self.start_orbiting)
        self.listener.accept_once("mouse2", self.start_panning)

    def start_orbiting(self):
        """
        Method to start orbiting
        """
        win_props = self.showbase.win.get_properties()
        w, h = win_props.get_x_size(), win_props.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        """ Store the mouse previous position"""
        self.mouse_prev = Point2(self.showbase.mouseWatcherNode.get_mouse())
        """ Add to task manager the orbit method """
        self.task_mgr.add(self.orbit, "transform_cam")
        """ Add mouse buttons to ignore or to accept only once to stop orbiting"""
        self.listener.ignore("mouse2")
        self.listener.ignore("mouse3")
        self.listener.accept_once("mouse1-up", self.stop_navigating)

    def orbit(self, task):
        """
        Orbit the camera about its target point by offsetting the orientation
        of the target node with the mouse motion.
        It captures the difference between the mouse previous position and the current
        and establishes a heading, a pitch and a roll value to the camera
        """

        if self.showbase.mouseWatcherNode.has_mouse():
            mouse_pos = self.showbase.mouseWatcherNode.get_mouse()
            speed_x, speed_y = self.orbit_speed
            """ Captures the heading and the pitch """
            d_h, d_p = (mouse_pos - self.mouse_prev)
            """ Increases the heading and the pitch by the speed x,y of the mouse"""
            d_h *= speed_x
            d_p *= speed_y
            """ Sets camera new angle """
            target = self.cam_target
            target.set_hpr(target.get_h() - d_h, target.get_p() + d_p, 0)
            self.mouse_prev = Point2(mouse_pos)

        return task.cont

    def zoom_step_in(self):
        """Translate the camera along its positive local Y-axis to zoom in"""

        target_dist = self.cam.get_y()
        self.cam.set_y(self.cam, -target_dist * .1)

    def zoom_step_out(self):
        """Translate the camera along its negative local Y-axis to zoom out"""

        target_dist = self.cam.get_y()
        self.cam.set_y(self.cam, target_dist * .1)

    def __get_pan_pos(self, pos):

        if not self.mouse_watcher.has_mouse():
            return False

        target = self.cam_target
        target_pos = target.get_pos()
        normal = self.world.get_relative_vector(target, Vec3(0., 1., 0.))
        plane = Plane(normal, target_pos)
        m_pos = self.mouse_watcher.get_mouse()
        near_point = Point3()
        far_point = Point3()
        self.cam_lens.extrude(m_pos, near_point, far_point)
        near_point = self.world.get_relative_point(self.cam, near_point)
        far_point = self.world.get_relative_point(self.cam, far_point)
        plane.intersects_line(pos, near_point, far_point)

        return True

    def start_panning(self):
        """ Method to initialize the pan process
        It starts ignoring the left button of the mouse and defining the stop
        condition (wheel up)
        """
        if not self.mouse_watcher.has_mouse():
            return

        self.listener.ignore("mouse1")
        self.listener.accept_once("mouse2-up", self.stop_navigating)
        self.__get_pan_pos(self.pan_start_pos)
        self.task_mgr.add(self.pan, "transform_cam")

    def pan(self, task):
        """ Method to set camera position

        :param: task: Task manager's task object
        :type task: :class:`direct.task`
        :return: Task.cont meaning it happens every frame
        """
        pan_pos = Point3()

        if not self.__get_pan_pos(pan_pos):
            return task.cont

        self.cam_target.set_pos(self.cam_target.get_pos() + (self.pan_start_pos - pan_pos))

        return task.cont
