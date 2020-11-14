import configparser
from multidict import CIMultiDict

cf = configparser.ConfigParser()
cf.read(
    "C:\\Users\\do\\Desktop\\source\\Machine-Learning\\DecisionTree\\config\\config.ini")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块


# secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，                        每个section由[]包裹，即[section])，并以列表的形式返回
# print(secs)

def getConfigerItems(section):
    return CIMultiDict(cf.items(section))


def getProjectConfig():
    return getConfigerItems("ProjectConfig")


c = getConfigerItems("ProjectConfig")
print(c.get("packagename"))
