from direct.gui.DirectGui import *
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser
from DirectGuiExtension.DirectGridSizer import DirectGridSizer

from view.grid import Grid


class Gui:
    """ Class holding all elements at the Graphical User Interface """

    def __init__(self, showbase):
        self.slider = DirectSlider(range=(0, 100), value=0, pageSize=3, scale=0.2,
                                   command=self.slider_grid_select,
                                   pos=(1.5, 0, -0.95))
        self.menu()


    def menu(self):
        """Configuring the menu file and architecture"""

        DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                         initialitem=0,
                         scale=.05,
                         textMayChange=0,
                         pos=(-1.7, 0, 0.95),
                         command=self.menu_option)

        DirectOptionMenu(items=['Arquitetura', 'Laje', 'Viga', 'Pilar', 'Fundação'],
                         initialitem=0,
                         scale=.05,
                         textMayChange=0,
                         pos=(-1.48, 0, 0.95))

    def menu_option(self, arg):
        """ Method to handle all the options of the menu

        :param arg: The caption of the menu selected
        :type arg: str
        """
        if arg == 'Novo':
            pass
        elif arg == 'Abrir':
            self.browser = DirectFolderBrowser(self.menu_open, fileBrowser=True)
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
            file = self.browser.get()
            self.browser.hide()
            self.browser.destroy()
            self.open_dialog = YesNoDialog(dialogName="OpenDialog", buttonTextList=['Sim', 'Não'],
                                 text="Deseja abrir " + file + "?", command=self.menu_open_file)
        if arg == False:
            self.browser.hide()
            self.browser.destroy()

    def menu_open_file(self, arg):
        """ Method to handle confirmation dialog to open file

        :param arg: The value ok = True, cancel = False
        :type arg: int
        """
        if arg:
            pass
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

    def slider_grid_select(self):
        Grid(base).draw_grid(spacing=round(self.slider['value'], 0))
