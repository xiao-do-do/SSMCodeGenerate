import pymysql
from dba.DBConnection import DBConnection
from helper import ConfigHelper


class MysqlConnectionImpl(DBConnection):
    def getConnection(self):
        ProjectConfig = ConfigHelper.getProjectConfig()
        mysqlUser = ProjectConfig.get("MysqlUser")
        mysqlPassword = ProjectConfig.get("MysqlPassword")
        mysqlDb = ProjectConfig.get("MysqlDb")
        MysqlHost = ProjectConfig.get("MysqlHost")
        conn = pymysql.connect(host=MysqlHost, user=mysqlUser, password=mysqlPassword, db=mysqlDb,
                               autocommit=True)
        return conn