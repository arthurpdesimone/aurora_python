from panda3d.core import NodePath, LineSegs, TextNode, VBase4, VBase3


class UCS:
    """ Create an UCS symbol on point (0,0,0) and draw a mini-UCS at the mouse position """
    def __init__(self, showbase):
        self.size = 1
        self.render = showbase.render
        self.create_ucs(5)

    def create_ucs(self, thickness=1):
        """ Create the UCS using the class :class:`panda3d.core.LineSegs`

        :param thickness: The UCS thickness
        :type thickness: int
        """
        ls = LineSegs('UCS')
        ls.setThickness(thickness)

        """ Draw three axes at once including the text"""
        label = ["x","y","z"]
        for i in range(3):
            color = VBase4(0,0,0,1)
            color[i] = 1
            ls.setColor(color)
            ls.moveTo(0,0,0)
            position = VBase3()
            position[i] = self.size
            ls.drawTo(position)
            text_node = TextNode("UCS")
            text = label[i]
            text_node.setText(text)
            text_node.setTextColor(color)
            text_node.setTextScale(0.25)

            text_node_path = NodePath(text_node)
            text_node_path.setPos(position)
            text_node_path.set_two_sided(True)
            text_node_path.reparentTo(self.render)

        node = ls.create()
        NodePath(node).reparentTo(self.render)


    def draw_cross(self,x,z,thickness=3):
        """ Method to create a tripod following the mouse cursor """

        ls = LineSegs('UCS mouse')
        ls.setThickness(thickness)
        size = 0.25
        """ Create mouse cursor at once"""
        for i in range(3):
            color = VBase4(0, 0, 0, 1)
            color[i] = 1
            ls.setColor(color)
            start = VBase3()
            start[i] = -size
            ls.moveTo(start)
            final = VBase3()
            final[i] = -start[i]
            ls.drawTo(final)

        node = ls.create()
        return NodePath(node)