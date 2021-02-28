import sys
from PIL import Image
from PyQt5 import QtGui, QtCore, QtWidgets
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import ClockObject, loadPrcFileData, GraphicsOutput, Texture, Point2, Point3, NodePath, LineSegs, TextNode
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode


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


class PandaApp(ShowBase):

    def __init__(self):

        # Set Panda3D configuration flags
        loadPrcFileData("", "window-type offscreen")

        ShowBase.__init__(self)

        self.physics_manager = BulletWorld()

        # Fill the dict with pairs like {'x': self.do_something}
        self.key_map = {}

        # Allow AI entities as much time as they need to think
        self.frame_rate = 60
        global globalClock
        globalClock.setMode(ClockObject.M_forced)
        globalClock.setFrameRate(self.frame_rate)
        globalClock.reset()

        # Necessary for scene visualization
        self.mouse_feature = ""
        self.start_mouse_work_fn = None
        self.stop_mouse_work_fn = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_steps = None

        # Instead of a window, we put the graphics to a texture which can be handled by other 3rd software like QT
        self.screen_texture = Texture()
        self.win.addRenderTexture(self.screen_texture, GraphicsOutput.RTMCopyRam)

        # Create the coords widget for indicating axes directions
        self.coords_np, self.axis_x_np, self.axis_y_np, self.axis_z_np, self.cam_label_np, self.cam_pos_np, self.cam_hpr_np, \
        self.touched_label_np, self.touched_object_np, self.touched_pos_np = self.create_screen_widgets()

        # Load the environment model.
        self.scene_np = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene_np.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene_np.setScale(0.25, 0.25, 0.25)
        self.scene_np.setPos(-8, 42, 0)


        # Create a ground for collisions
        shape = BulletPlaneShape((0, 0, 1), 3)
        ground_node = BulletRigidBodyNode("ground-node")
        ground_node.addShape(shape)
        self.physics_manager.attachRigidBody(ground_node)
        ground_np = self.scene_np.attachNewNode(ground_node)

        # Adjust the scene elements
        self.setBackgroundColor(Color3D.White)
        self.disable_mouse()
        self.cam.setPos(10, -25, 15)
        self.cam.lookAt(0, 0, 0)
        self.camera_pivot_np = self.render.attachNewNode("camera_pivot")
        self.camera_pivot_np.setPos(self.get_point_from_cam_lens((0, 0))[1])
        self.cam.reparentTo(self.camera_pivot_np)

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        time_per_frame = self.get_time_per_frame()
        self.update_camera()
        self.physics_manager.doPhysics(time_per_frame)
        return Task.cont

    def get_time_per_frame(self):
        return globalClock.getDt()

    def start_mouse_work(self, feature, start_mouse_work_fn, stop_mouse_work_fn):
        self.mouse_feature = feature
        self.start_mouse_work_fn = start_mouse_work_fn
        self.stop_mouse_work_fn = stop_mouse_work_fn
        self.cam_label_np.show()
        self.cam_pos_np.show()
        self.cam_hpr_np.show()
        self.touched_label_np.show()
        self.touched_object_np.show()
        self.touched_pos_np.show()

        # Pick a position to act as pivot to the camera
        if self.mouse_feature == "zoom":
            target_pos = (self.mouse_x, self.mouse_y)
        else:
            target_pos = (0, 0)
        self.touched_object, self.touched_pos = self.get_point_from_cam_lens(target_pos)
        if self.touched_pos is not None:
            # Move camera pivot to touched position
            cam_pos = self.cam.getPos(self.render)
            self.cam.reparentTo(self.render)
            self.camera_pivot_np.setPos(self.touched_pos)
            self.cam.reparentTo(self.camera_pivot_np)
            self.cam.setPos(self.render, cam_pos)

            self.start_mouse_work_fn()

    def stop_mouse_work(self):
        self.mouse_feature = ""
        self.last_mouse_x = None
        self.last_mouse_y = None
        self.cam_label_np.hide()
        self.cam_pos_np.hide()
        self.cam_hpr_np.hide()
        self.touched_label_np.hide()
        self.touched_object_np.hide()
        self.touched_pos_np.hide()

        self.stop_mouse_work_fn()

    def update_camera(self):
        # Use mouse input to turn/move the camera.
        if self.mouse_feature != "":
            diff_x = (self.last_mouse_x - self.mouse_x) if self.last_mouse_x is not None else 0
            diff_y = (self.last_mouse_y - self.mouse_y) if self.last_mouse_y is not None else 0
            self.last_mouse_x = self.mouse_x
            self.last_mouse_y = self.mouse_y
            if self.mouse_feature == "rotate":
                offset = 5000 * self.get_time_per_frame()
                self.camera_pivot_np.setH(self.camera_pivot_np.getH() + diff_x * offset)  # horizontal plane
                self.camera_pivot_np.setR(self.camera_pivot_np.getR() - diff_y * offset)  # vertical plane
            elif self.mouse_feature == "pan":
                offset = 15000 * self.get_time_per_frame()
                self.camera_pivot_np.setZ(self.cam, self.camera_pivot_np.getZ(self.cam) + diff_y * offset)  # horizontal plane
                self.camera_pivot_np.setX(self.cam, self.camera_pivot_np.getX(self.cam) + diff_x * offset)  # vertical plane
            elif self.mouse_feature == "zoom":
                offset = 0.1 * self.get_time_per_frame()
                diff = self.cam.getPos(self.render) - self.camera_pivot_np.getPos(self.render)
                self.cam.setPos(self.render, self.cam.getPos(self.render) - diff * self.mouse_steps * offset)
                self.stop_mouse_work()

            # Format the camera info text
            cam_pos = tuple([round(n, 2) for n in self.cam.getPos(self.render)])
            cam_hpr = tuple([round(n, 2) for n in self.cam.getHpr(self.render)])
            cam_pos_text = "XYZ: ({:d}, {:d}, {:d})".format(int(cam_pos[0]), int(cam_pos[1]), int(cam_pos[2]))
            cam_hpr_text = "HPR: ({:d}, {:d}, {:d})".format(int(cam_hpr[0]), int(cam_hpr[1]), int(cam_hpr[2]))

            # Update coordinates widget
            hpr = self.render.getHpr(self.cam)
            self.coords_np.setHpr(hpr)
            hpr = self.cam.getHpr(self.render)
            self.axis_x_np.setHpr(hpr)
            self.axis_y_np.setHpr(hpr)
            self.axis_z_np.setHpr(hpr)

            # Show camera position and rotation
            self.cam_pos_np.node().setText(cam_pos_text)
            self.cam_hpr_np.node().setText(cam_hpr_text)

            # Format the touch info text showing object and point touched by the cross
            touched_object_text = ""
            touched_pos_text = ""
            if self.touched_object is not None:
                touched_object_text = "Name: " + self.touched_object.getParent(0).getName()
            if self.touched_pos is not None:
                touched_pos_text = "XYZ: ({:d}, {:d}, {:d})".format(int(self.touched_pos[0]),
                                                                    int(self.touched_pos[1]),
                                                                    int(self.touched_pos[2]))
            self.touched_object_np.node().setText(touched_object_text)
            self.touched_pos_np.node().setText(touched_pos_text)

    def get_point_from_cam_lens(self, target_pos):

        # Get to and from pos in camera coordinates and transform to global coordinates
        p_from, p_to = Point3(), Point3()
        self.camLens.extrude(Point2(target_pos), p_from, p_to)
        p_from = self.render.getRelativePoint(self.cam, p_from)
        p_to = self.render.getRelativePoint(self.cam, p_to)

        # Get the target coordinates which correspond to mouse coordinates and walk the camera to this direction
        result = self.physics_manager.rayTestClosest(p_from, p_to)
        if result.hasHit():
            return result.getNode(), result.getHitPos()
        else:
            return None, None

    def create_screen_widgets(self):

        # Pin the coords in left-bottom of the screen
        origin = [-1.4, 5, -0.85]
        coords_np, axis_x_np, axis_y_np, axis_z_np = create_axes_cross("coords", 3, True)
        coords_np.reparentTo(self.cam)
        coords_np.setPos(self.cam, tuple(origin))
        coords_np.setScale(0.1)

        # Put the camera label ('observer') text in the left-bottom corner
        origin = [-1.7, 5, -1.1]
        text = TextNode("cam_label")
        text.setText("Observer")
        text.setTextColor(Color3D.Yellow)
        cam_label_np = self.cam.attachNewNode(text)
        cam_label_np.setPos(self.cam, tuple(origin))
        cam_label_np.setScale(0.07)

        # Put the camera position in the left-bottom corner
        origin = [-1.7, 5, -1.2]
        text = TextNode("cam_pos")
        text.setText("XYZ:")
        text.setTextColor(Color3D.Yellow)
        cam_pos_np = self.cam.attachNewNode(text)
        cam_pos_np.setPos(self.cam, tuple(origin))
        cam_pos_np.setScale(0.07)

        # Put the camera rotation in the left-bottom corner
        origin = [-1.7, 5, -1.3]
        text = TextNode("cam_hpr")
        text.setText("HPR:")
        text.setTextColor(Color3D.Yellow)
        cam_hpr_np = self.cam.attachNewNode(text)
        cam_hpr_np.setPos(self.cam, tuple(origin))
        cam_hpr_np.setScale(0.07)

        # Put the touch label text in the right-bottom corner
        origin = [0.8, 5, -1.1]
        text = TextNode("touched_label")
        text.setText("Touched Object")
        text.setTextColor(Color3D.Yellow)
        touched_label_np = self.cam.attachNewNode(text)
        touched_label_np.setPos(self.cam, tuple(origin))
        touched_label_np.setScale(0.07)

        # Put the touched objected in the right-bottom corner
        origin = [0.8, 5, -1.2]
        text = TextNode("touched_object")
        text.setText("Name:")
        text.setTextColor(Color3D.Yellow)
        touched_object_np = self.cam.attachNewNode(text)
        touched_object_np.setPos(self.cam, tuple(origin))
        touched_object_np.setScale(0.07)

        # Put the touched point in the right-bottom corner
        origin = [0.8, 5, -1.3]
        text = TextNode("touched_pos")
        text.setText("Pos:")
        text.setTextColor(Color3D.Yellow)
        touched_pos_np = self.cam.attachNewNode(text)
        touched_pos_np.setPos(self.cam, tuple(origin))
        touched_pos_np.setScale(0.07)

        return coords_np, axis_x_np, axis_y_np, axis_z_np, cam_label_np, cam_pos_np, cam_hpr_np, touched_label_np, touched_object_np, touched_pos_np


class SimulationWindow(QtWidgets.QWidget):

    def __init__(self, panda_app):
        QtWidgets.QWidget.__init__(self)
        self.panda_app = panda_app
        self.init_ui()
        self.update_timer.start()

    def init_ui(self):

        # viewer_3d
        self.viewer_3d = Viewer3D(self.panda_app)
        self.viewer_3d.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # update_timer
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.setInterval(1)
        self.update_timer.timeout.connect(self.viewer_3d.update)

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.viewer_3d)

        # Window
        self.setLayout(layout)
        self.setWindowTitle("Simulation")
        self.setToolTip("Left-Button-Pressed: Rotate\r\nMiddle-Button-Pressed: Pan\r\nWheel: Zoom in/out")


class Viewer3D(QtWidgets.QLabel):

    def __init__(self, panda_app):
        QtWidgets.QLabel.__init__(self)
        self.panda_app = panda_app
        self.mouse_working_area = None
        self.mouse_inside_working_area = False
        self.pixel_map = None
        self.init_ui()

    def init_ui(self):

        # pivot
        self.pivot = QtWidgets.QLabel(self)
        self.pivot.setText("+")
        self.pivot.setFont(QtGui.QFont('Arial', 20))
        self.pivot.setStyleSheet("QLabel { color : yellow }")
        self.pivot.setVisible(False)


        # Change background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)

        # self
        self.setPalette(palette)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

    def update(self):

        # Forward a step on Panda simulation
        self.panda_app.taskMgr.step()

        # Get the image to be draw on this viewer.
        texture = self.panda_app.screen_texture
        size = (texture.getXSize(), texture.getYSize())
        print(size)
        format = "RGBA"
        if texture.mightHaveRamImage():
            image = Image.frombuffer(format, size, texture.getRamImageAs(format), "raw", format, 0, 0)
        else:
            image = Image.new(format, size)

        # Draw the image.
        _image = image.toqimage()
        self.pixel_map = QtGui.QPixmap.fromImage(_image)
        self.adjust_mouse_working_area()

    def adjust_mouse_working_area(self):
        if self.pixel_map is not None:
            viewer_size = self.size()
            self.setPixmap(self.pixel_map.scaled(viewer_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            image_size = self.pixmap().size()
            horizontal_margin = (viewer_size.width() - image_size.width()) / 2
            vertical_margin = (viewer_size.height() - image_size.height()) / 2
            self.mouse_working_area = (horizontal_margin,
                                       vertical_margin,
                                       horizontal_margin + image_size.width(),
                                       vertical_margin + image_size.height())

    def resizeEvent(self, event):
        self.adjust_mouse_working_area()

    def handle_key_event(self, event, event_state):
        # Inform Panda to start (or continue) the action associated with the key pressed
        # or stop it if key is released
        key_pressed = event.key()

        # Check if key is in the user's key map an then call associated function
        for k, value in self.panda_app.key_map.items():
            if "-" in k:
                [key_ascii, key_state] = k.split("-")
            else:
                key_ascii = k
                key_state = ""
            if key_state == event_state and QtGui.QKeySequence(key_ascii) == key_pressed and not event.isAutoRepeat():
                (func, args) = value
                func(*args)
                break

    def keyPressEvent(self, event):
        self.handle_key_event(event, "")

    def keyReleaseEvent(self, event):
        self.handle_key_event(event, "up")

    def create_start_mouse_work_fn(self, x, y):
        def fn():
            width = 20
            height = 20
            self.pivot.setGeometry(x - (width / 2), y - (height / 2), width, height)
            self.pivot.setVisible(True)
        return fn

    def create_stop_mouse_work_fn(self):
        def fn():
            self.pivot.setVisible(False)
        return fn

    def mouseMoveEvent(self, event):
        if self.mouse_working_area is not None:
            def pyqt_to_panda(val, max):
                mid = max / 2
                return (val - mid) / float(mid)

            # Check if mouse is on the image
            mouse_pos = event.pos()
            x, y = mouse_pos.x(), mouse_pos.y()
            x0, y0, xn, yn = self.mouse_working_area
            if self.mouse_working_area is not None and x >= x0 and x <= xn and y >= y0 and y <= yn:
                self.mouse_inside_working_area = True
            else:
                self.mouse_inside_working_area = False

            # Fix coordinates by removing margins of PyQT screen
            x -= x0
            y -= y0
            width = xn - x0
            height = yn - y0

            # Transform coordinates from PyQt (0, n) to Panda (-1, 1)
            self.panda_app.mouse_x = pyqt_to_panda(x, width)
            self.panda_app.mouse_y = pyqt_to_panda(y, height) * (-1)

            # Pass the movement commands to Panda
            if self.mouse_inside_working_area and self.panda_app.mouse_feature == "":
                feature = ""
                if event.buttons() == QtCore.Qt.LeftButton:
                    feature = "rotate"
                elif event.buttons() == QtCore.Qt.MiddleButton:
                    feature = "pan"
                if feature != "":
                    start_fn = self.create_start_mouse_work_fn(self.width() / 2, self.height() / 2)
                    stop_fn = self.create_stop_mouse_work_fn()
                    self.panda_app.start_mouse_work(feature, start_fn, stop_fn)

    def mouseReleaseEvent(self, event):
        self.panda_app.stop_mouse_work()

    def wheelEvent(self, event):
        if self.mouse_inside_working_area:
            mouse_pos = event.pos()
            start_fn = self.create_start_mouse_work_fn(mouse_pos.x(), mouse_pos.y())
            stop_fn = self.create_stop_mouse_work_fn()
            self.panda_app.start_mouse_work("zoom", start_fn, stop_fn)
            self.panda_app.mouse_steps = event.angleDelta().y()


def main():

    # Initialize Qt environment
    pyqt_app = QtWidgets.QApplication(sys.argv)

    # Run Panda
    panda_app = PandaApp()

    # Start the Qt environment
    simulation_window = SimulationWindow(panda_app)
    simulation_window.showMaximized()

    sys.exit(pyqt_app.exec_())


if __name__ == "__main__":
    main()