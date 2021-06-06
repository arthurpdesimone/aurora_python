from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QPushButton
from qt_material import apply_stylesheet
from view.gui.Themes import *

class HotkeyDialog(QDialog):
    def __init__(self):
        super(HotkeyDialog, self).__init__()
        self.main = uic.loadUi('hotkeys.ui', self)
        apply_stylesheet(self, theme=DARK_TEAL)
        """ Highlight all the buttons """
        buttons = self.main.findChildren(QPushButton)
        for b in buttons:
            b.setStyleSheet("QPushButton::hover {background-color : teal;}")
