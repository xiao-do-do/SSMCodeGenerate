from Observable import Observable
from db.Mapper import Mapper


class Generator(Observable):
    def __init__(self, con, config):
        self.sqlMap = Mapper(conn=con, config=config)
        self.maps = self.sqlMap.readDatabaseMaps()

    def go(self):
        super().go(self.maps)
