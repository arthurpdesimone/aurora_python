from direct.gui.DirectGui import *
class Gui:
    def __init__(self, showbase):
        self.slider = DirectSlider(range=(0, 100), value=0, pageSize=3, scale=0.2,
                                   command=self.value_grid_select,
                                    pos=(1.6, 0, -0.95))

    def value_grid_select(self):
        print(round(self.slider['value'],1))