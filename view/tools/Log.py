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

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance