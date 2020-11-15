import copy
import os

from jinja2 import FileSystemLoader, Environment

from Observable import Observer
from utils.utils import file_name, bindFilters, doNone


class EntifyFile(Observer):
    def __init__(self, obj):
        obj.add(self)

    def __init__(self):
        pass

    def add(self, obj):
        obj.add(self)

    def update(self, maps):
        tables = maps["listTables"]
        descs = maps["listDesc"]

        print(tables)
        print(descs)

        tableInfos = maps["tableInfo"]

        listTemplate = file_name("templates")

        for jk in listTemplate:
            for tableInfo in tableInfos:
                # 渲染两次第一次是为了将渲染结果放到全局变量
                # 第二次渲染savePath将第一次渲染结果写入文件

                path = '{}/templates/'.format(os.path.dirname(__file__))
                loader = FileSystemLoader(path)
                env = Environment(loader=loader)
                # 创建一个加载器, jinja2 会从这个目录中加载模板

                bindFilters(env)

                env2 = copy.deepcopy(env)
                env2.filters['saveFile'] = doNone

                renderRes = env2.get_template(jk).render(tableInfo=tableInfo)

                # 把渲染你结果存到env全局变量this里，
                env.globals['this'] = renderRes

                # 再次渲染写入this这个结果到文件
                env.get_template(jk).render(tableInfo=tableInfo)

    pass
