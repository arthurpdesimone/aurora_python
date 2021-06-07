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
            if b.toolTip() != "":
                print(self.remove_html_markup(b.toolTip()))
                b.setStyleSheet("QPushButton {background-color : teal;}")
            else:
                b.setStyleSheet("QPushButton::hover {background-color : teal;}")

    def remove_html_markup(self,s):
        """ Method to strip html text from html code"""
        tag = False
        quote = False
        out = ""

        for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

        return out