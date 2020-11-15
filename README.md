# SSMCodeGenerate
 SSM数据表逆向生成代码，使用jinja2模板引擎更灵活

如何使用
=

    #Main.py
    
    # 首先需要config/config.ini修改数据库信息
    projectConfig = ConfigHelper.getProjectConfig()
    conn = MariadbConnectionImpl().getConnection()
   
    # 获取数据库链接,和项目信息传递给生成器
    generator = Generator(conn, projectConfig)
    templates = Templates()
    generator.add(templates)
    generator.go()

文件简介
=
config

    config.ini 为配置信息

db

    impl        数据库链接的实现
    Mapper      映射数据表
    TableInfo   数据表封装
    
helper

    ConfigHelper    从config.ini中读取配置信息
    
templates
        
    生成模板
        
utils

    绑定到jinj2模板引擎中的一些过滤器，可以在模板中使用这些方法
    

    
        
