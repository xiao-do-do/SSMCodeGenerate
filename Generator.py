from Observable import Observable
from Mapper import Mapper


class Generator(Observable):
    def __init__(self, con, config):
        self.sqlMap = Mapper(conn=con, config=config)
        self.maps = self.sqlMap.getSqlMaps()

    def go(self):
        super().go(self.maps)
