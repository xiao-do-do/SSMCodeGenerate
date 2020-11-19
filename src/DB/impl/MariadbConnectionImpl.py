from db.DBConnection import DBConnection
from db.impl.MysqlConnectionImpl import MysqlConnectionImpl


class MariadbConnectionImpl(DBConnection):
    def getConnection(self):
        sqlConn = MysqlConnectionImpl()
        return sqlConn.getConnection()
