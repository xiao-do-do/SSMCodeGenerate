from utils import ConfigReader


# 数据表信息
class TableInfo(object):
    savePackageName = ConfigReader.getProjectConfig().get("PackageName")
    saveModelName = "entity"
    packageName = savePackageName + "." + saveModelName
    fullColumn = []
    # 表所有字段
    otherColumn = []
    # 表非主键字段
    pkColumn = ""
    pkColumnUpper = ""
    # 主键字段
    pkShortType = ""
    # 主键JAVA类型
    foreignInfo = []

    name = ""
    # 表名
    nameUpper = ""



    pass


# 数据表字段信息
class ColumnInfo(object):
    name = ""
    fullType = ""
    shortType = ""
    jdbcType = ""
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
