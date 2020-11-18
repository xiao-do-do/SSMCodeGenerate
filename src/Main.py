from Templates import Templates
from Generator import Generator
from utils import ConfigReader
from db.impl.MariadbConnectionImpl import MariadbConnectionImpl

if __name__ == '__main__':
    # 首先需要config/config.ini修改数据库信息
    projectConfig = ConfigReader.getProjectConfig()
    conn = MariadbConnectionImpl().getConnection()
    # 获取数据库链接,和项目信息传递给生成器

    generator = Generator(conn, projectConfig)
    templates = Templates()
    generator.add(templates)
    generator.go()
