from direct.gui.DirectGui import *
class Gui:
    """ Class holding all elements at the Graphical User Interface """
    def __init__(self, showbase):
        self.slider = DirectSlider(range=(0, 100), value=0, pageSize=3, scale=0.2,
                                   command=self.value_grid_select,
                                    pos=(1.6, 0, -0.95))
        self.menu()

    def menu(self):
        """Configuring the menu file and architecture"""

        DirectOptionMenu(items=['Arquivo', 'Novo', 'Abrir', 'Salvar', 'Fechar'],
                         initialitem=0,
                         scale=.05,
                         textMayChange=0,
                         pos=(-1.93, 0, 0.96))

        DirectOptionMenu(items=['Arquitetura', 'Laje', 'Viga', 'Pilar', 'Fundação'],
                         initialitem=0,
                         scale=.05,
                         textMayChange=0,
                         pos=(-1.71, 0, 0.96))

    def value_grid_select(self):
        print(round(self.slider['value'],1))