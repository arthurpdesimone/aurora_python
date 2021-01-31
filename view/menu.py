# Class to control menus
from direct.gui.DirectGui import *
class Menu:
    #Constructor
    def __init__(self, showbase):
        # Configuring the menu file
        DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                                     initialitem=0,
                                     scale=.05,
                                     textMayChange=0,
                                     pos=(-1.93, 0, 0.96))

        # Configuring the menu architecture
        DirectOptionMenu(items=['Arquitetura', 'Laje', 'Viga', 'Pilar', 'Fundação'],
                                    initialitem=0,
                                    scale=.05,
                                    textMayChange=0,
                                    pos=(-1.71, 0, 0.96))