# 数据表字段信息封装
from BaseInfo import BaseInfo


class ColumnInfo(BaseInfo):
    name = ""
    # 字段名
    fullType = ""
    # JAVA完整类型
    shortType = ""
    # JAVA类型
    jdbcType = ""
    # 数据库中类型
    null = ""
    # 是否可为空
    primaryKey = ""
    # 是否主键
    exTra = ""
    # 附加属性
