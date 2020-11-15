from EntityFile import EntifyFile
from Generator import Generator
from helper import ConfigHelper
from dba.impl.MariadbConnectionImpl import MariadbConnectionImpl

if __name__ == '__main__':
    # 首先需要config/config.ini修改数据库信息

    projectConfig = ConfigHelper.getProjectConfig()
    conn = MariadbConnectionImpl().getConnection()
    # 获取数据库链接,和项目信息传递给生成器

    generator = Generator(conn, projectConfig)
    generator.add(EntifyFile())
    generator.go()
