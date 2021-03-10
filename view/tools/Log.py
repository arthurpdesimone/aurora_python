from datetime import datetime


class Log:
    """ Class to manage all events that happens inside the program"""
    _instance = None

    def __init__(self):
        self.log = {}

    def appendLog(self,message):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        self.log[timestamp] = message
        print(self.log)

    def printRenderChild(self,render):
        for children in render.getChildren():
            print(children)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance