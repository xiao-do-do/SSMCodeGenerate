from helper import ConfigHelper


# 数据表信息
class TableInfo(object):
    savePackageName = ConfigHelper.getProjectConfig().get("PackageName")
    saveModelName = "entity"
    packageName = savePackageName + "." + saveModelName
    fullColumn = []
    pkShortType = ""
    otherrColumn = []
    forignInfo = []

    # 常用数据格式
    name = ""
    nameUpper = ""
    pkColumn = ""
    pkColumnUpper = ""

    pass


# 数据表字段信息
class ColumnInfo(object):
    name = "asdf"
    fullType = "java.lang.Object"
    shortType = "Object"
    null = ""
    primaryKey = ""
    exTra = ""

    pass


# 数据表外键信息
class ForignInfo(object):
    ownTableName = ""
    ownColumn = ""
    targetTableName = ""
    targetColumn = ""
    constraintName = ""
    joinTablesColumn = []

    pass
