from panda3d.core import Point2, Point3, Plane, Vec3

from lang.Language import *
from view.tools.Log import Log


class Camera:
    """ Class to control the camera of the showbase """
    log = Log.instance()

    def __init__(self, showbase):
        self.showbase = showbase
        self.task_mgr = showbase.task_mgr
        self.mouse_watcher = showbase.mouseWatcherNode
        self.world = showbase.render
        self.cam = showbase.camera
        self.cam_lens = showbase.camLens
        self.cam_target = showbase.render.attach_new_node("Target")
        self.cam.reparent_to(self.cam_target)
        self.mouse_prev = Point2()
        w, h = showbase.win.get_x_size(), showbase.win.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        self.pan_start_pos = Point3()
        self.zoom_step_factor = 10  # additional zoom step multiplier
        self.accept_commands()
        self.showbase.accept("remove_camera",self.remove_commands)
        self.showbase.accept("accept_camera", self.accept_commands)

    def accept_commands(self):
        """ Key bindings to control the camera"""
        self.showbase.accept_once("mouse1", self.start_orbiting)
        self.showbase.accept_once("mouse3", self.start_panning)
        self.showbase.accept("wheel_up", self.zoom_step_in)
        self.showbase.accept("wheel_down", self.zoom_step_out)
        self.showbase.accept("w", self.zoom_y_increase_const)
        self.showbase.accept("s", self.zoom_y_decrease_const)
        self.showbase.accept("a", self.zoom_x_decrease_const)
        self.showbase.accept("d", self.zoom_x_increase_const)
        self.showbase.accept("q", self.zoom_z_decrease_const)
        self.showbase.accept("e", self.zoom_z_increase_const)
        self.showbase.accept("r", self.reset_camera)


    def remove_commands(self):
        """ Remove all key bindings """
        self.showbase.ignore("mouse1")
        self.showbase.ignore("mouse3")
        self.showbase.ignore("wheel_up")
        self.showbase.ignore("wheel_down")
        self.showbase.ignore("w")
        self.showbase.ignore("a")
        self.showbase.ignore("s")
        self.showbase.ignore("d")
        self.showbase.ignore("q")
        self.showbase.ignore("e")
        self.showbase.ignore("r")

    def reset_camera(self):
        """ Method to reset the camera to its initial position"""
        self.cam.set_x(2)
        self.cam.set_y(-10)
        self.cam.set_z(2)
        self.cam.set_hpr(0,0,0)

    def stop_navigating(self):
        """ Method to stop orbiting or panning """
        self.task_mgr.remove("transform_cam")
        self.showbase.accept_once("mouse1", self.start_orbiting)
        self.showbase.accept_once("mouse3", self.start_panning)

    def start_panning(self):
        if not self.mouse_watcher.hasMouse():
            return

        self.showbase.ignore("mouse1")
        self.showbase.accept_once("mouse3-up", self.stop_navigating)
        self.__get_pan_pos(self.pan_start_pos)
        self.task_mgr.add(self.pan, "transform_cam")


    def start_orbiting(self):
        """ Method to start orbit task"""
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
            self.print_status(ORBIT)

        return task.cont

    def zoom_step_in(self):
        """Translate the camera along its positive local Y-axis to zoom in"""

        target_dist = self.cam.get_y()
        self.cam.set_y(self.cam, -target_dist * .1)
        self.print_status(Y_DECREASE_EXPONENTIAL)

    def zoom_step_out(self):
        """Translate the camera along its negative local Y-axis to zoom out"""

        target_dist = self.cam.get_y()
        self.cam.set_y(self.cam, target_dist * .1)
        self.print_status(Y_INCREASE_EXPONENTIAL)

    def zoom_y_increase_const(self):
        """Increase y position of camera using a constant step value"""

        current_dist = self.cam.get_y()
        new_dist = current_dist + .1 * self.zoom_step_factor
        self.cam.set_y(new_dist)
        self.print_status(Y_INCREASE_CONSTANT)

    def zoom_y_decrease_const(self):
        """Decrease y position of camera using a constant step value"""

        current_dist = self.cam.get_y()
        new_dist = current_dist - .1 * self.zoom_step_factor
        self.cam.set_y(new_dist)
        self.print_status(Y_DECREASE_CONSTANT)

    def zoom_x_decrease_const(self):
        """Increase x position of camera using a constant step value"""

        current_dist = self.cam.get_x()
        new_dist = current_dist - .1 * self.zoom_step_factor
        self.cam.set_x(new_dist)
        self.print_status(X_DECREASE_CONSTANT)

    def zoom_x_increase_const(self):
        """Decrease x position of camera using a constant step value"""

        current_dist = self.cam.get_x()
        new_dist = current_dist + .1 * self.zoom_step_factor
        self.cam.set_x(new_dist)
        self.print_status(X_INCREASE_CONSTANT)

    def zoom_z_increase_const(self):
        """Increase y position of camera using a constant step value"""

        current_dist = self.cam.get_z()
        new_dist = current_dist + .1 * self.zoom_step_factor
        self.cam.set_z(new_dist)
        self.print_status(Z_INCREASE_CONSTANT)

    def zoom_z_decrease_const(self):
        """Decrease y position of camera using a constant step value"""

        current_dist = self.cam.get_z()
        new_dist = current_dist - .1 * self.zoom_step_factor
        self.cam.set_z(new_dist)
        self.print_status(Z_DECREASE_CONSTANT)

    def __get_pan_pos(self, pos):
        """ Method to get pan position
        :param pos: :class: panda3d.core.Point3D """

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

    def pan(self, task):
        """ Method to pan """
        pan_pos = Point3()

        if not self.__get_pan_pos(pan_pos):
            return task.cont

        self.cam.set_pos(self.cam.get_pos() + (self.pan_start_pos - pan_pos))
        self.print_status(PAN)

        return task.cont

    def print_status(self, action=''):
        self.log.appendLog(action+' - Camera : POS '+
                           str(self.cam.get_pos()).replace('LPoint3f','')+
                           str(self.cam.get_hpr()).replace('LVecBase3f',' HPR '))
