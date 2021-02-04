from panda3d.core import NodePath, LineSegs, TextNode

class UCS:
    """ Create an UCS symbol on point (0,0,0) """
    def __init__(self, showbase):
        self.size = 2
        self.render = showbase.render
        self.P3DCreateAxes(5)
        self.UCS_text()

    def P3DCreateAxes(self,thickness=1):
        """ Create the UCS using the class :class:`panda3d.core.LineSegs`

        :param thickness: The UCS thickness
        :type thickness: int
        """
        ls = LineSegs()
        ls.setThickness(thickness)

        """ X axis """
        ls.setColor(1.0, 0.0, 0.0, 1.0)
        ls.moveTo(0.0, 0.0, 0.0)
        ls.drawTo(self.size, 0.0, 0.0)

        """ Y axis """
        ls.setColor(0.0, 1.0, 0.0, 1.0)
        ls.moveTo(0.0, 0.0, 0.0)
        ls.drawTo(0.0, self.size, 0.0)

        """ Z axis """
        ls.setColor(0.0, 0.0, 1.0, 1.0)
        ls.moveTo(0.0, 0.0, 0.0)
        ls.drawTo(0.0, 0.0, self.size)

        node = ls.create()
        NodePath(node).reparentTo(self.render)

    def UCS_text(self):
        """ Draw X, Y, Z at the tip of each of the UCS axis"""

        txt_x = TextNode('xText')
        txt_x.setText("x")
        txt_x_node = self.text_customize(txt_x)
        txt_x_node.setPos(self.size, 0, 0)
        # y text
        txt_y = TextNode('yText')
        txt_y.setText("y")
        txt_y_node = self.text_customize(txt_y)
        txt_y_node.setPos(0, self.size, 0)
        # z text
        txt_z = TextNode('zText')
        txt_z.setText("z")
        txt_z_node = self.text_customize(txt_z)
        txt_z_node.setPos(0, 0, self.size)

    def text_customize(self,text_node):
        # Configuring aspects to a black background
        text_node.setFrameColor(0, 0, 0, 1)
        text_node.setCardColor(0, 0, 0, 1)
        text_node.setCardAsMargin(0.4, 0.4, 0.4, 0.4)
        text_node.setCardDecal(True)
        # Creating a NodePath object
        text_node_path = NodePath(text_node)
        text_node_path.setScale(0.25)
        text_node_path.reparentTo(self.render)
        return text_node_path

    def draw_cross(self,x,z,thickness=3):
        ls = LineSegs()
        ls.setThickness(thickness)
        size = 0.25

        # X axis
        ls.setColor(1.0, 0.0, 0.0, 1.0)
        ls.moveTo(-size, 0.0, 0.0)
        ls.drawTo(size, 0.0, 0.0)

        # Y axis
        ls.setColor(0.0, 1.0, 0.0, 1.0)
        ls.moveTo(0.0, -size, 0.0)
        ls.drawTo(0.0, size, 0.0)

        # Z axis
        ls.setColor(0.0, 0.0, 1.0, 1.0)
        ls.moveTo(0.0,0.0,-size)
        ls.drawTo(0.0,0.0,size)
        node = ls.create()

        return NodePath(node)