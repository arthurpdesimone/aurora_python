from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

ShowBase()

base.cTrav = CollisionTraverser()

collHandEvent = CollisionHandlerEvent()
collHandEvent.addInPattern('into-%in')

smiley = loader.loadModel('models/smiley')
smiley.reparentTo(render)
smiley.setPos(5, 25, 0)
smiley.setTag('smileyTag', '1')

cNode = CollisionNode('smiley')
cNode.addSolid(CollisionSphere(0, 0, 0, 1))
smileyC = smiley.attachNewNode(cNode)

pickerNode = CollisionNode('mouseRay')
pickerNP = camera.attachNewNode(pickerNode)
pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
pickerRay = CollisionRay()
pickerNode.addSolid(pickerRay)
base.cTrav.addCollider(pickerNP, collHandEvent)


def click():
    mpos = base.mouseWatcherNode.getMouse()
    pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
    base.cTrav.traverse(render)

    base.accept('into-smiley', print, ['Smiley Clicked!'])


base.accept('mouse1', click)

base.run()