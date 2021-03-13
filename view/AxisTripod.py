from panda3d.core import *


class AxisTripod:
    """ Class to draw an interactive camera UCS tripod"""
    def __init__(self, showbase):
        self._buffer = showbase.buff
        self._dr_pixel_size = 100  # size of display region in pixels
        dr = self._buffer.make_display_region(0, 1., 0., 1.)
        dr.sort = 2
        lens = OrthographicLens()
        lens.film_size = .235

        self._cam_target = cam_target = NodePath("tripod_cam_target")
        cam_target.set_compass(showbase.cam)
        cam_node = Camera("tripod_cam")
        camera = cam_target.attach_new_node(cam_node)

        camera.node().set_lens(lens)
        dr.camera = camera
        dr.set_clear_color_active(False)
        dr.set_clear_depth_active(True)
        self._display_region = dr

        self._root = camera.attach_new_node("world_axes")
        self._root.set_y(10.)
        self.model = self.create_model()

        node = self._root.node()
        node.set_bounds(OmniBoundingVolume())
        node.final = True

        self._buffer_size = (0, 0)
        showbase.task_mgr.do_method_later(.2, self.update_region_size, "update_region_size")

    def create_model(self):

        vertex_format = GeomVertexFormat.get_v3c4()

        vertex_data = GeomVertexData("axis_tripod_data", vertex_format, Geom.UH_static)
        pos_writer = GeomVertexWriter(vertex_data, "vertex")
        col_writer = GeomVertexWriter(vertex_data, "color")

        lines = GeomLines(Geom.UH_static)
        for i in range(3):
            v_pos = VBase3()
            pos_writer.add_data3(v_pos)
            v_pos[i] = .1
            pos_writer.add_data3(v_pos)
            color = VBase4(0., 0., 0., 1.)
            color[i] = 1.
            col_writer.add_data4(color)
            col_writer.add_data4(color)
            lines.add_vertices(i * 2, i * 2 + 1)

        geom = Geom(vertex_data)
        geom.add_primitive(lines)
        node = GeomNode("axis_tripod")
        node.add_geom(geom)

        model = self._root.attach_new_node(node)

        return model

    def update_region_size(self, task):

        win_w, win_h = self._buffer.size

        if self._buffer_size == (win_w, win_h):
            return task.again

        aspect_ratio = win_w / win_h
        size_h = self._dr_pixel_size / win_w
        size_v = size_h * aspect_ratio
        self._buffer_size = (win_w, win_h)
        self._display_region.dimensions = (0., size_h, 0., size_v)

        return task.again