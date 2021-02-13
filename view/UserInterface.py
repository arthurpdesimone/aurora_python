from direct.gui.DirectGui import *
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectMenuItem import DirectMenuItem, DirectMenuItemEntry, DirectMenuItemSubMenu
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser
from dxf.dxf import DXF
from view.AutoSizer import AutoSizer


class UserInterface:
    """ Class holding all elements at the Graphical User Interface """

    def __init__(self, showbase):
        self.showbase = showbase
        self.mainBox = DirectBoxSizer(orientation=DGG.VERTICAL, autoUpdateFrameSize=False)
        AutoSizer(child=self.mainBox,extendHorizontal=False,childUpdateSizeFunc=self.mainBox.refresh)
        self.menu()
        """Let the GUI system create the layout"""
        self.file = ''


    def menu(self):
        """Configuring the menu file"""
        fileList = [
            DirectMenuItemEntry("Novo", print, [False]),
            DirectMenuItemEntry("Abrir", print, [True]),
            DirectMenuItemSubMenu("Importar >", [
                DirectMenuItemEntry("Abrir DXF", self.menu_option, ["Abrir DXF"]),
                DirectMenuItemEntry("Limpar DXF", self.menu_option, ["Limpar DXF"]),
            ]),
            DirectMenuItemEntry("Fechar", self.menu_option, ["Fechar"])]
        fileMenu = DirectMenuItem(text="Arquivo", scale=0.07, item_relief=2, items=fileList)

        """Configuring the menu architecture"""
        archList = [
            DirectMenuItemEntry("Laje", print, [False]),
            DirectMenuItemEntry("Viga", print, [True]),
            DirectMenuItemEntry("Pilar", self.menu_option, ["Fechar"]),
            DirectMenuItemEntry("Fundação", self.menu_option, ["Fechar"])
        ]
        archMenu = DirectMenuItem(text="Arquitetura", scale=0.07, item_relief=2, items=archList)
        """Configuring the menu loads"""
        loadList = [
            DirectMenuItemEntry("Carga em área", print, [False]),
            DirectMenuItemEntry("Carga em linha", print, [True]),
            DirectMenuItemEntry("Carga em ponto", self.menu_option, ["Fechar"]),
            DirectMenuItemEntry("Carga térmica", self.menu_option, ["Fechar"])
        ]
        loadMenu = DirectMenuItem(text="Cargas", scale=0.07, item_relief=2, items=loadList)
        boxSizer = DirectBoxSizer(itemAlign=DirectBoxSizer.A_Left)
        boxSizer.addItem(fileMenu)
        boxSizer.addItem(archMenu)
        boxSizer.addItem(loadMenu)

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