# Aurora python
# Aiding civil engineers to build reinforced concrete buildings

from pandac.PandaModules import WindowProperties
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath, LineSegs, TextNode, Point3, Point2, Vec3, Plane
import win32gui, win32con

class CameraController:

    def __init__(self, showbase):

        self.showbase = showbase
        self.task_mgr = showbase.task_mgr
        self.mouse_watcher = showbase.mouseWatcherNode
        self.world = showbase.render
        self.cam = showbase.camera
        self.cam_lens = showbase.camLens
        self.cam_target = showbase.render.attach_new_node("camera_target")
        self.cam.reparent_to(self.cam_target)
        self.cam.set_y(-10.)
        self.mouse_prev = Point2()
        win_props = showbase.win.get_properties()
        w, h = win_props.get_x_size(), win_props.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        self.pan_start_pos = Point3()
        self.listener = listener = DirectObject()
        listener.accept_once("mouse1", self.start_orbiting)
        listener.accept_once("mouse3", self.start_panning)
        listener.accept("wheel_up", self.zoom_step_in)
        listener.accept("wheel_down", self.zoom_step_out)

    def stop_navigating(self):

        self.task_mgr.remove("transform_cam")
        self.listener.accept_once("mouse1", self.start_orbiting)
        self.listener.accept_once("mouse3", self.start_panning)

    def start_orbiting(self):

        win_props = self.showbase.win.get_properties()
        w, h = win_props.get_x_size(), win_props.get_y_size()
        self.orbit_speed = (w * .15, h * .15)
        self.mouse_prev = Point2(self.mouse_watcher.get_mouse())
        self.task_mgr.add(self.orbit, "transform_cam")
        self.listener.ignore("mouse3")
        self.listener.accept_once("mouse1-up", self.stop_navigating)

    def orbit(self, task):
        """
        Orbit the camera about its target point by offsetting the orientation
        of the target node with the mouse motion.

        """

        if self.mouse_watcher.has_mouse():
            mouse_pos = self.mouse_watcher.get_mouse()
            speed_x, speed_y = self.orbit_speed
            d_h, d_p = (mouse_pos - self.mouse_prev)
            d_h *= speed_x
            d_p *= speed_y
            target = self.cam_target
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

        if not self.mouse_watcher.has_mouse():
            return

        self.listener.ignore("mouse1")
        self.listener.accept_once("mouse3-up", self.stop_navigating)
        self.__get_pan_pos(self.pan_start_pos)
        self.task_mgr.add(self.pan, "transform_cam")

    def pan(self, task):

        pan_pos = Point3()

        if not self.__get_pan_pos(pan_pos):
            return task.cont

        self.cam_target.set_pos(self.cam_target.get_pos() + (self.pan_start_pos - pan_pos))

        return task.cont

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #To enable the camera
        self.disable_mouse()
        #Maximizing window
        self.hwnd = win32gui.GetForegroundWindow()
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)
        camera = CameraController(self)

app = App()

def drawGrid(x_lines=100,y_lines=100,spacing=2):
    ls = LineSegs()
    ls.setThickness(1)
    ls.setColor(1.0,1.0,1.0,0.5)


def P3DCreateAxes(lineThickness=1):
    ls = LineSegs()
    ls.setThickness(lineThickness)

    # X axis
    ls.setColor(1.0, 0.0, 0.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(1.0, 0.0, 0.0)

    # Y axis
    ls.setColor(0.0, 1.0, 0.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(0.0, 1.0, 0.0)

    # Z axis
    ls.setColor(0.0, 0.0, 1.0, 1.0)
    ls.moveTo(0.0, 0.0, 0.0)
    ls.drawTo(0.0, 0.0, 1.0)

    node = ls.create()
    return NodePath(node)

#Format X,Y,Z text indications
def UCS_text():
    # x text
    txt_x = TextNode('xText')
    txt_x.setText("x")
    txt_x_node = text_customize(txt_x)
    txt_x_node.setPos(1, 0, 0)
    # y text
    txt_y = TextNode('yText')
    txt_y.setText("y")
    txt_y_node = text_customize(txt_y)
    txt_y_node.setPos(0, 1, 0)
    # z text
    txt_z = TextNode('zText')
    txt_z.setText("z")
    txt_z_node = text_customize(txt_z)
    txt_z_node.setPos(0, 0, 1)

def text_customize(text_node):
    # Configuring aspects to a black background
    text_node.setFrameColor(0, 0, 0, 1)
    text_node.setCardColor(0, 0, 0, 1)
    text_node.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
    text_node.setCardDecal(True)
    # Creating a NodePath object
    text_node_path = NodePath(text_node)
    text_node_path.setScale(0.15)
    text_node_path.reparentTo(app.render)
    return text_node_path

# Configuring the menu file
file_menu = DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                             initialitem=0,
                             scale=.05,
                             textMayChange=0,
                             pos=(-0.96, 0, 0.96))

# Configuring the menu architecture
arq_menu = DirectOptionMenu(items=['Arquitetura', 'Laje', 'Viga', 'Pilar', 'Fundação'],
                            initialitem=0,
                            scale=.05,
                            textMayChange=0,
                            pos=(-0.74, 0, 0.96))



ucs = P3DCreateAxes(3)
ucs.reparentTo(app.render)
UCS_text()


# Configuring window
props = WindowProperties()
props.setTitle('Aurora Python')
app.win.requestProperties(props)
app.setBackgroundColor(0, 0, 0)
# Configuration of camera and running
app.camera.setPos(4,-10,2)
app.run()
