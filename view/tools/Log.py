from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtWidgets import QTextEdit


class Log:
    """ Class to manage all events that happens inside the program"""
    _instance = None

    def __init__(self):
        self.log = {}
        self.text_area = None

    def appendLog(self,message):
        """ Method to append a message to the log object"""
        now = datetime.now()
        now_formatted = now.strftime('%Y-%m-%d %H:%M:%S')
        self.log[now_formatted] = message
        self._update_text_area()

    def _update_text_area(self):
        self.text_area.clear()
        log = ""
        for time, message in self.log.items():
            log += f"{time} : {message}\n"
        self.text_area.setText(log)
        self.text_area.moveCursor(QtGui.QTextCursor.End)

    def sync_text_area(self,text_area):
        self.text_area = text_area

    def render_children(self,render):
        list_children = list()
        for children in render.getChildren():
            list_children.append(children.getName())
        return list_children

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance