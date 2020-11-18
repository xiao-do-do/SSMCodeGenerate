import configparser

from multidict import CIMultiDict

cf = configparser.ConfigParser()
cf.read("config/config.ini")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块


def getConfigerItems(section):
    return CIMultiDict(cf.items(section))


def getProjectConfig():
    return getConfigerItems("ProjectConfig")


def getTypeMapperConfig():
    return getConfigerItems("typeMapper")
