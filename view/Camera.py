from panda3d.core import WindowProperties, Point2, Point3, Plane, Vec3

from view.tools.Log import Log


class Camera:
    def __init__(self, showbase):
        self.showbase = showbase
        self.task_mgr = showbase.task_mgr
        self.mouse_watcher = showbase.mouseWatcherNode
        self.world = showbase.render
        self.cam = showbase.camera
        self.cam_lens = showbase.camLens
        self.cam_target = showbase.render.attach_new_node("Target")
        self.cam.reparent_to(self.cam_target)
        self.cam.set_y(-10.)
        self.mouse_prev = Point2()
        w, h = showbase.win.get_x_size(), showbase.win.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        self.pan_start_pos = Point3()
        self.zoom_step_factor = 10  # additional zoom step multiplier
        self.showbase.accept_once("mouse1", self.start_orbiting)
        self.showbase.accept_once("mouse3", self.start_panning)
        self.showbase.accept("wheel_up", self.zoom_step_in)
        self.showbase.accept("wheel_down", self.zoom_step_out)
        self.showbase.accept("arrow_up", self.zoom_step_in_const)
        self.showbase.accept("arrow_down", self.zoom_step_out_const)
        self.showbase.accept("arrow_left", self.left_step_in_const)
        self.showbase.accept("arrow_right", self.right_step_in_const)
        self.showbase.accept("-", self.decr_zoom_step_factor)
        self.showbase.accept("+", self.incr_zoom_step_factor)

    def stop_navigating(self):

        self.task_mgr.remove("transform_cam")
        self.showbase.accept_once("mouse1", self.start_orbiting)
        self.showbase.accept_once("mouse3", self.start_panning)

    def start_orbiting(self):
        w, h = self.showbase.screenTexture.x_size, self.showbase.screenTexture.y_size
        self.orbit_speed = (w * .15, h * .15)
        self.mouse_prev = Point2(self.mouse_watcher.getMouse())
        self.task_mgr.add(self.orbit, "transform_cam")
        self.showbase.ignore("mouse3")
        self.showbase.accept_once("mouse1-up", self.stop_navigating)

    def orbit(self, task):
        """
        Orbit the camera about its target point by offsetting the orientation
        of the target node with the mouse motion.

        """

        if self.mouse_watcher.hasMouse():
            mouse_pos = self.mouse_watcher.getMouse()
            speed_x, speed_y = self.orbit_speed
            d_h, d_p = (mouse_pos - self.mouse_prev)
            d_h *= speed_x
            d_p *= speed_y
            target = self.cam
            target.set_hpr(target.get_h() - d_h, target.get_p() + d_p, 0.)
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

    def zoom_step_in_const(self):
        """Zoom in using a constant step value"""

        current_dist = self.cam.get_y()
        new_dist = current_dist + .1 * self.zoom_step_factor

        # Prevent the camera to move past its target node
        # if new_dist > -.01:
        #    new_dist = -.01

        self.print_status('zoom step in')

        self.cam.set_y(new_dist)

    def zoom_step_out_const(self):
        """Zoom out using a constant step value"""

        current_dist = self.cam.get_y()
        new_dist = current_dist - .1 * self.zoom_step_factor

        self.print_status('zoom step out')
        self.cam.set_y(new_dist)

    def left_step_in_const(self):
        """Zoom in using a constant step value"""

        current_dist = self.cam.get_x()
        new_dist = current_dist - .1 * self.zoom_step_factor

        # Prevent the camera to move past its target node
        # if new_dist > -.01:
        #    new_dist = -.01


        self.cam.set_x(new_dist)

    def right_step_in_const(self):
        """Zoom out using a constant step value"""

        current_dist = self.cam.get_x()
        new_dist = current_dist + .1 * self.zoom_step_factor

        self.cam.set_x(new_dist)

    def decr_zoom_step_factor(self):
        """Decrease the value with which to multiply the zoom steps"""

        self.zoom_step_factor -= 1  # Or some value that you prefer

        # Prevent the multiplier from becoming too small
        if self.zoom_step_factor < .1:
            self.zoom_step_factor = .1

        print("self.zoom_step_factor:", self.zoom_step_factor)

    def incr_zoom_step_factor(self):
        """Increase the value with which to multiply the zoom steps"""

        self.zoom_step_factor += .1  # Or some value that you prefer
        print("self.zoom_step_factor:", self.zoom_step_factor)

    def __get_pan_pos(self, pos):

        if not self.mouse_watcher.hasMouse():
            return False

        target = self.cam_target
        target_pos = target.get_pos()
        normal = self.world.get_relative_vector(target, Vec3(0., 1., 0.))
        plane = Plane(normal, target_pos)
        m_pos = self.mouse_watcher.getMouse()
        near_point = Point3()
        far_point = Point3()
        self.cam_lens.extrude(m_pos, near_point, far_point)
        near_point = self.world.get_relative_point(self.cam, near_point)
        far_point = self.world.get_relative_point(self.cam, far_point)
        plane.intersects_line(pos, near_point, far_point)

        return True

    def start_panning(self):

        if not self.mouse_watcher.hasMouse():
            return

        self.showbase.ignore("mouse1")
        self.showbase.accept_once("mouse3-up", self.stop_navigating)
        self.__get_pan_pos(self.pan_start_pos)
        self.task_mgr.add(self.pan, "transform_cam")

    def pan(self, task):

        pan_pos = Point3()

        if not self.__get_pan_pos(pan_pos):
            return task.cont

        self.cam.set_pos(self.cam.get_pos() + (self.pan_start_pos - pan_pos))
        self.print_status('pan')

        return task.cont

    def print_status(self, action=''):
        print(action, ' - Camera :', self.cam.get_pos(), " Target :", self.cam_target.getPos())