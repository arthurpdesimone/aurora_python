from database.DatabaseManager import DatabaseManager


class Model:
    """ Singleton to handle a single model """
    _instance = None

    def __init__(self):
        self.db = None
        self.beams = {}
        self.columns = {}
        self.footings = {}
        self.slabs = {}
        self.materials = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def init_db(self,file):
        DatabaseManager(file)