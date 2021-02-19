import sys
import ezdxf
from panda3d.core import LPoint3f, LineSegs, NodePath


class DXF:
    """ Class to manipulate DXF drawings and transform then into 3D objects"""

    def __init__(self, showbase):
        self.app = showbase

    def read_dxf(self,path,digits=2):
        """ Method to read DXF elements and convert into a 3D model

        :param path: File path
        :type path: str
        :param digits: The number of digits to round DXF coordinates
        :type digits: int
        :return:
        """
        try:
            doc = ezdxf.readfile(path)
            msp = doc.modelspace()
            for e in msp:
                """ If a line is found"""
                if e.dxftype() == 'LINE':
                    thickness = 3
                    color = (1, 1, 1, 0.1)
                    start_point = e.dxf.start
                    end_point = e.dxf.end
                    ls = LineSegs('DXF')
                    ls.setThickness(thickness)
                    ls.setColor(color)

                    start = LPoint3f(round(start_point.x,digits),
                                     round(start_point.y,digits),
                                     round(start_point.z,digits))
                    end = LPoint3f(round(end_point.x, digits),
                                     round(end_point.y, digits),
                                     round(end_point.z, digits))

                    ls.moveTo(start.x,start.y,start.z)
                    ls.drawTo(end.x,end.y,end.z)

                    node = ls.create()
                    node_path = NodePath(node)
                    node_path.reparentTo(self.app.render)

        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)

    def save_dxf(self,path):
        pass

    def clear_dxf(self):
        for children in self.app.render.getChildren():
            if children.getName() == 'DXF':
                children.removeNode()