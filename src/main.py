from EntityFile import EntifyFile
from Generator import Generator
from helper import ConfigHelper
from DB.DBImpl.MysqlConnectionImpl import MysqlConnectionImpl

if __name__ == '__main__':
    projectConfig = ConfigHelper.getProjectConfig()
    conn = MysqlConnectionImpl().getConnection()
    # 获取数据库链接,和项目信息传递给生成器

    generator = Generator(conn, projectConfig)
    generator.add(EntifyFile())
    generator.go()
