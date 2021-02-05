import sys
import ezdxf


try:
    doc = ezdxf.readfile("C:\\rectangle.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)


def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)
# iterate over all entities in modelspace
msp = doc.modelspace()
for e in msp:
    if e.dxftype() == 'LINE':
        print_entity(e)

# entity query for all LINE entities in modelspace
for e in msp.query('LINE'):
    print_entity(e)

