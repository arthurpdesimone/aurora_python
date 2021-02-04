import random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode, loadPrcFileData
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectEntry import DirectEntry
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectGridSizer import DirectGridSizer
from DirectGuiExtension.DirectScrolledWindowFrame import DirectScrolledWindowFrame
from DirectGuiExtension.DirectMenuItem import DirectMenuItem, DirectMenuItemEntry, DirectMenuItemSubMenu
from DirectGuiExtension.DirectTooltip import DirectTooltip
from DirectGuiExtension.DirectSpinBox import DirectSpinBox
from DirectGuiExtension.DirectDiagram import DirectDiagram
from DirectGuiExtension.DirectDatePicker import DirectDatePicker
from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
from DirectGuiExtension import DirectGuiHelper as DGH

from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

loadPrcFileData(
    "",
    """
    window-title DirectGUI Extensions Demo
    show-frame-rate-meter #t
    """)


app = ShowBase()


# MAIN LAYOUT
mainBox = DirectBoxSizer(orientation=DGG.VERTICAL, autoUpdateFrameSize=False)
DirectAutoSizer(child=mainBox, childUpdateSizeFunc=mainBox.refresh)


# CALENDAR EXAMPLE
# in a function to be called by a menu item
def showCalendar():
    dp = DirectDatePicker()
    calendarDragFrame = DirectScrolledWindowFrame(frameSize=dp["frameSize"])
    dp.reparentTo(calendarDragFrame)
    dp.refreshPicker()
    calendarDragFrame.setPos(-calendarDragFrame.getWidth()*0.5,0,calendarDragFrame.getHeight()*0.5)


# BROWSER EXAMPLE
# tooltip to be used in the browser
tt = DirectTooltip(parent=pixel2d, text_scale=12, frameColor=(1, 1, 0.7, 1), pad=(5,5))
# in a function to be called by a menu item
def showBrowser(doLoad):
    dragFrame = DirectScrolledWindowFrame(parent=pixel2d, frameSize=(-250,250,-200,200), dragAreaHeight=25, pos=(260,0,-300), closeButtonScale=20)
    def accept(ok):
        print(ok)
        dragFrame.destroy()
    DirectFolderBrowser(accept, doLoad, tooltip=tt, parent=dragFrame)


# MENU ITEMS
itemList = [
    DirectMenuItemEntry("Save", showBrowser, [False]),
    DirectMenuItemEntry("Load", showBrowser, [True]),
    DirectMenuItemSubMenu("Recent >", [
        DirectMenuItemEntry("Item A", print, ["Item A"]),
        DirectMenuItemEntry("Item B", print, ["Item B"]),
        DirectMenuItemEntry("Item C", print, ["Item C"])
    ]),
    DirectMenuItemEntry("Quit", quit, [])]
fileMenu = DirectMenuItem(text="File", scale=0.1, item_relief=1, items=itemList)
itemList = [
    DirectMenuItemEntry("Show Calendar", showCalendar, []),
    DirectMenuItemEntry("Help", print, ["Help"])]
viewMenu = DirectMenuItem(text="View", scale=0.1, item_relief=1, items=itemList)

boxSizer = DirectBoxSizer(itemAlign=DirectBoxSizer.A_Center)
boxSizer.addItem(fileMenu)
boxSizer.addItem(viewMenu)

mainBox.addItem(boxSizer)


# GRID SIZER
gridSizer = DirectGridSizer(numRows=4, numColumns=5, autoUpdateFrameSize=True, itemMargin=[0.01, 0.01, 0.01, 0.01])

def createButton(txt):
    btn = DirectButton(
        text=txt,
        text_scale=0.1,
        borderWidth=(0.01, 0.01),
        frameColor=(0.7,0.7,0.7,1),
        frameSize=(-0.1,0.1,-0.07,0.125),
        command=base.messenger.send,
        extraArgs=["updateEntry", [txt]],
        )
    return btn

gridSizer.addItem(createButton("7"), 0,0)
gridSizer.addItem(createButton("8"), 0,1)
gridSizer.addItem(createButton("9"), 0,2)
gridSizer.addItem(createButton("4"), 1,0)
gridSizer.addItem(createButton("5"), 1,1)
gridSizer.addItem(createButton("6"), 1,2)
gridSizer.addItem(createButton("1"), 2,0)
gridSizer.addItem(createButton("2"), 2,1)
gridSizer.addItem(createButton("3"), 2,2)
gridSizer.addItem(createButton("0"), 3,1)
gridSizer.addItem(createButton("*"), 0,3)
gridSizer.addItem(createButton("-"), 1,3)
gridSizer.addItem(createButton("+"), 2,3)
gridSizer.addItem(createButton("="), 3,3)
gridSizer.addItem(createButton("/"), 0,4)
gridSizer.addItem(createButton("CE"), 1,4)
gridSizer.addItem(createButton("c"), 2,4)

gridBox = DirectBoxSizer(
    autoUpdateFrameSize=False,
    frameSize=(0,0,-DGH.getRealHeight(gridSizer)/2,DGH.getRealHeight(gridSizer)/2),
    itemAlign=DirectBoxSizer.A_Center
    )
gridBox.addItem(gridSizer)
gridAutoSizer = DirectAutoSizer(extendVertical=False, child=gridBox, childUpdateSizeFunc=gridBox.refresh)

entry = DirectEntry(scale=.1, text_align=TextNode.ARight, relief=DGG.SUNKEN, overflow=False)
entry["state"] = DGG.DISABLED
entryBox = DirectBoxSizer(
    autoUpdateFrameSize=False,
    frameSize=(0,0,-DGH.getRealHeight(entry)/2,DGH.getRealHeight(entry)/2),
    itemAlign=DirectBoxSizer.A_Center
    )
entryBox.addItem(entry)
entryAutoSizer = DirectAutoSizer(extendVertical=False, child=entryBox, childUpdateSizeFunc=entryBox.refresh)

def updateEntry(arg):
    if arg == "=":
        entry.set(str(eval(entry.get())))
    elif arg == "c":
        entry.set(entry.get()[:-1])
    elif arg == "CE":
        entry.set("")
    else:
        entry.set(entry.get() + arg)

app.accept("updateEntry", updateEntry)

mainBox.addItem(entryAutoSizer)
mainBox.addItem(gridAutoSizer)


# SPINNER
spinBox = DirectSpinBox(pos=(0.8,0,0.25), value=0, minValue=-10, maxValue=10, repeatdelay=0.125, buttonOrientation=DGG.HORIZONTAL, valueEntry_text_align=TextNode.ACenter, borderWidth=(.1,.1))
spinBox.setScale(0.1)
spinBox["relief"] = 2
spinBoxSizer = DirectBoxSizer(
    orientation=DGG.VERTICAL,
    autoUpdateFrameSize=False,
    frameSize=(0,0,spinBox["frameSize"][2]*spinBox.getScale()[0]*2,spinBox["frameSize"][3]*spinBox.getScale()[0]*2),
    itemAlign=DirectBoxSizer.A_Center|DirectBoxSizer.A_Middle
    )
spinerInfo = DirectLabel(text="Change diagram value range: ", scale=0.1)
spinBoxSizer.addItem(spinerInfo)
spinBoxSizer.addItem(spinBox)
spinAutoSizer = DirectAutoSizer(extendVertical=False, child=spinBoxSizer, childUpdateSizeFunc=spinBoxSizer.refresh)
mainBox.addItem(spinAutoSizer)


# DIAGRAM
data = [10, -5, 1, -1, 1, -1, 1, -1, 1, -1]
height = (1+mainBox.itemsBottom)/2
dd = DirectDiagram(
    data=data,
    numberAreaWidth=0.15,
    numNegSteps=20,
    numPosSteps=20,
    numNegStepsStep=2,
    numPosStepsStep=2,
    stepFormat=int,
    numtextScale=0.04,
    frameSize=(-.25, .25, -height, height))
diagramAutoSizer = DirectAutoSizer(parent=mainBox, extendVertical=False, child=dd)
mainBox.addItem(diagramAutoSizer)
def updateTask(task):
    global data
    data = data[1:]
    data += [random.uniform(-10+spinBox.getValue(), 10+spinBox.getValue())]
    dd["data"] = data
    return task.again

base.taskMgr.doMethodLater(0.25, updateTask, "updateDiagram")



app.run()