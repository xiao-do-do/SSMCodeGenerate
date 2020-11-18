import os

# 获取文件夹下所有的文件
from datetime import datetime


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.template':  # 想要保存的文件格式
                L.append(file)
    return L


# 下划线转驼峰
def str2Hump(text):
    if len(text) > 0:
        text[0]
        arr = filter(None, text.lower().split('_'))
        res = ''
        j = 0
        for i in arr:
            if j == 0:
                res = i
            else:
                res = res + i[0].upper() + i[1:]
            j += 1
        return res
    else:
        return "没主键？"


# 首字母转大写
def capitalize(string, lower_rest=False):
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


# 首字母大写，其余字母转小写
def capitalizeLower(string, lower_rest=True):
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


# 转大写
def upper(tmpStr):
    return str(tmpStr).upper()


# 转小写
def lower(tmpstr):
    return str(tmpstr).lower()


# 小驼峰命令
def camelCase(tmpStr):
    return str2Hump(tmpStr)


# 大驼峰命名
def CamelCase(tmpStr):
    return capitalize(str2Hump(tmpStr))


# 保存文件
def saveFile(data, moduleName, fileName):
    # print("------------")
    # print(data)
    # print(moduleName)
    # print(fileName)
    print("[INFO] 保存文件 -> %s/%s" % (moduleName, fileName))
    if not os.path.exists(moduleName):
        os.makedirs(moduleName)

    with open(moduleName + "\\" + fileName, 'w') as file_object:
        file_object.write(data)


# 什么也不做
def doNone(age, moduleName, fileName):
    return ""


def currTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


#
# def initDir(config):
#     prefix = "java"
#     listPackage = config.get("PackageList").split(",")
#     for i in listPackage:
#         if not os.path.exists("%s/%s" % (prefix, i)):
#             os.makedirs("%s/%s" % (prefix, i))

# 将一些函数绑定到jinja2环境中，即可在模板中使用模板中
def bindFilters(env):
    env.filters['camelCase'] = camelCase
    env.filters['CamelCase'] = CamelCase
    env.filters['saveFile'] = saveFile
    env.filters['lower'] = lower
    env.filters['upper'] = upper
    env.filters['capitalizeLower'] = capitalizeLower
    env.filters['capitalize'] = capitalize
    env.filters['currTime'] = currTime
