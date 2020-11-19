import abc

from utils import ConfigReader

# 数据表信息
from utils.Utils import CamelCase, pascalCase, camelCase, appendAttr


class BaseInfo(metaclass=abc.ABCMeta):
    # 反射获取所有str属性，并且设置对应的不同命名方式的值。
    def appendSelfAttr(self):
        for attrs in dir(self):
            if not attrs.startswith("__") and (isinstance(attrs, str)):
                strAttr = getattr(self, attrs)
                if isinstance(strAttr, str):
                    appendAttr(self, attrs, strAttr)

                elif isinstance(strAttr, BaseInfo):
                    c = getattr(strAttr, "appendSelfAttr")
                    c()

                elif isinstance(strAttr, list):
                    for dd in strAttr:
                        if isinstance(dd, BaseInfo):
                            c = getattr(dd, "appendSelfAttr")
                            c()


# 数据表字段信息
class ColumnInfo(BaseInfo):
    name = ""
    fullType = ""
    shortType = ""
    jdbcType = ""
    null = ""
    primaryKey = ""
    exTra = ""


class TableInfo(BaseInfo):
    savePackageName = ConfigReader.getProjectConfig().get("PackageName")
    saveModelName = "entity"
    packageName = savePackageName + "." + saveModelName
    fullColumn = []
    # 表所有字段
    otherColumn = []
    # 表非主键字段
    pkColumn = ColumnInfo()
    # 主键字段
    pkShortType = ""
    # 主键JAVA类型
    foreignInfo = []
    name = ""




# 数据表外键信息
class ForignInfo(BaseInfo):
    ownTableName = ""
    ownColumn = ""
    targetTableName = ""
    targetColumn = ""
    constraintName = ""
    joinTablesColumn = []

    # def appendSelfAttr(self):
    #     appendAttr(self, "ownTableName", self.ownTableName)
    #     appendAttr(self, "ownColumn", self.ownColumn)
    #     appendAttr(self, "targetTableName", self.targetTableName)
    #     appendAttr(self, "targetColumn", self.targetColumn)
    #     # appendAttr(self, "constraintName", self.constraintName)
    #
    # pass
