from direct.gui.DirectGui import *
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser
from DirectGuiExtension.DirectMenuItem import DirectMenuItemEntry, DirectMenuItem, DirectMenuItemSubMenu
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

from dxf.dxf import DXF
from view.directgui import GUI, Widget, Sizer


class UserInterface:
    """ Class holding all elements at the Graphical User Interface """

    def __init__(self, showbase):
        self.showbase = showbase
        # MAIN LAYOUT
        self.mainBox = DirectBoxSizer(orientation=DGG.VERTICAL, autoUpdateFrameSize=False)
        DirectAutoSizer(child=self.mainBox, childUpdateSizeFunc=self.mainBox.refresh)
        """The root node of all DirectGui widgets needs to be pixel2d in order to work
        with the automatic layout system"""
        # self.gui_root = gui_root = showbase.pixel2d
        """Initialize the GUI system"""
        # self.gui = gui = GUI(showbase)

        """Build the GUI layout"""

        """Add a horizontally expanding title bar"""
        # self.label = DirectLabel(parent=gui_root, text="", frameSize=(0, 0, -15, 30),
        #                     text_scale=20, borderWidth=(0, 0), relief=DGG.SUNKEN)
        # widget = Widget(self.label)
        # borders = (0, 0, 0, 0)
        """By default, the title bar will take up all of the width and height of its
        cell (the default value for the `alignments` parameter of the `Sizer.add`
        method is `("expand", "expand")`), but the cell itself still needs to be
        able to take up the entire width of the window; this is done by setting
        the horizontal proportion (which gets applied to the cell's column) to a
        value bigger than zero"""
        # gui.sizer.add(widget, proportions=(1., 0.), borders=borders)

        """Add a horizontally growable sizer that will be expanded horizontally"""
        # self.frame_area_sizer = sizer = Sizer("horizontal")
        # borders = (10, 10, 20, 10)
        # gui.sizer.add(sizer, proportions=(1., 0.), borders=borders)
        #
        #
        # self.has_frame = True
        #
        # self.__add_menu()
        self.menu()
        """Let the GUI system create the layout"""
        #self.menu()
        self.file = ''
        # gui.layout()


    def menu(self):
        """Configuring the menu file and architecture"""
        # create menu structure
        # MENU ITEMS
        itemList = [
            DirectMenuItemEntry("Save", print, [False]),
            DirectMenuItemEntry("Load", print, [True]),
            DirectMenuItemSubMenu("Recent >", [
                DirectMenuItemEntry("Item A", print, ["Item A"]),
                DirectMenuItemEntry("Item B", print, ["Item B"]),
                DirectMenuItemEntry("Item C", print, ["Item C"])
            ]),
            DirectMenuItemEntry("Quit", quit, [])]
        fileMenu = DirectMenuItem(text="File", scale=0.1, item_relief=1, items=itemList)
        itemList = [
            DirectMenuItemEntry("Show Calendar", print, []),
            DirectMenuItemEntry("Help", print, ["Help"])]
        viewMenu = DirectMenuItem(text="View", scale=0.1, item_relief=1, items=itemList)

        boxSizer = DirectBoxSizer(itemAlign=DirectBoxSizer.A_Center)
        boxSizer.addItem(fileMenu)
        boxSizer.addItem(viewMenu)

        self.mainBox.addItem(boxSizer)

    def menu_option(self, arg):
        """ Method to handle all the options of the menu

        :param arg: The caption of the menu selected
        :type arg: str
        """
        print(arg)

        if arg == 'Novo':
            pass
        elif arg == 'Abrir DXF':
            self.browser = DirectFolderBrowser(self.menu_open, fileBrowser=True, defaultPath='C:\\')
        elif arg == 'Limpar DXF':
            DXF(self.showbase).clear_dxf()
        elif arg == 'Fechar':
            self.close_dialog = YesNoDialog(dialogName="CloseDialog", buttonTextList=['Sim', 'Não'],
                                      text="Deseja fechar o programa?", command=self.menu_close_file)

    def menu_open(self, arg):
        """Method to handle DirectFolderBrowser and open a file to the model
        https://github.com/fireclawthefox/DirectFolderBrowser

        :param arg: The value ok = True, cancel = False
        :type arg: int
        """
        if arg == True:
            # print the selected file
            self.file = self.browser.get()
            self.browser.hide()
            self.browser.destroy()
            self.open_dialog = YesNoDialog(dialogName="OpenDialog", buttonTextList=['Sim', 'Não'],
                                 text="Deseja abrir " + self.file + "?", command=self.menu_open_file)
        if arg == False:
            self.browser.hide()
            self.browser.destroy()

    def menu_open_file(self, arg):
        """ Method to handle confirmation dialog to open file

        :param arg: The value ok = True, cancel = False
        :type arg: int
        """
        if arg:
            DXF(self.showbase).read_dxf(self.file)
        else:
            pass
        self.open_dialog.cleanup()

    def menu_close_file(self, arg):
        """ Method to handle confirmation dialog to close application

        :param arg: The value ok = True, cancel = False
        :type arg: int
        """
        if arg:
            exit()
        else:
            self.close_dialog.cleanup()

    def __add_menu(self):

        if not self.has_frame:
            return

        DirectOptionMenu(parent=self.gui_root, text="options", scale=20,
                                borderWidth=(0, 0), items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'], initialitem=0,
                                frameSize=(1, 1, -1, -1.5), highlightColor=(.65, .65, .65, 1.), textMayChange=0,
                                text_pos=(1, -1), popupMarkerBorder=(1, -1),command=self.menu_option)

        DirectOptionMenu(parent=self.gui_root, text="options", scale=20,
                         borderWidth=(0, 0), items=['Arquitetura','Abrir DXF','Limpar DXF', 'Laje', 'Viga', 'Pilar', 'Fundação'], initialitem=0,
                         frameSize=(5, 5, -1, -1.5), highlightColor=(.65, .65, .65, 1.),textMayChange=0,
                         text_pos=(5, -1), popupMarkerBorder=(1, -1), command=self.menu_option)

