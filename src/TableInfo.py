from BaseInfo import BaseInfo


# 表封装
from ColumnInfo import ColumnInfo


class TableInfo(BaseInfo):
    name = ""
    # 表名
    fullColumns = []
    # 表所有字段
    otherColumns = []
    # 表非主键字段
    pkColumn = ColumnInfo()
    # 主键字段
    pkShortType = ""
    # 主键JAVA类型
    foreignInfos = []


