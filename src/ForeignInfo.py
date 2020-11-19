# 数据表外键信息封装
from BaseInfo import BaseInfo


class ForeignInfo(BaseInfo):
    ownTableName = ""
    # 自己的表名
    ownColumn = ""
    # 自己外键
    targetTableName = ""
    # 约束目标表名
    targetColumn = ""
    # 约束目标建
    constraintName = ""
    # 约束名称
    joinTablesColumns = []
    # 两个表所有属性集合
