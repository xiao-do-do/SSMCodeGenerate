import copy
import re

from multidict import CIMultiDict

from ColumnInfo import ColumnInfo
from ForeignInfo import ForeignInfo
from TableInfo import TableInfo
from utils import ConfigReader


def getTypeMapper(mapType):
    # 从config.ini中寻找与数据库相匹配的JAVA数据类型
    typeMapper = ConfigReader.getTypeMapperConfig()
    for i in typeMapper:
        if r"\(" in i:
            pattern = re.compile(i)
            result1 = pattern.findall(mapType)
            if result1:
                return typeMapper[i]
        else:
            if i == mapType:
                return typeMapper[i]
        pass


def getShortTypeMapper(mapType):
    # 把Sql的字段的类型转为JAVA类型
    strType = getTypeMapper(mapType)
    if strType:
        cnt = str(strType).rfind(".")
        return strType[cnt + 1:]


def getColumnFromTableInfos(TableInfos, tableName):
    for ab in TableInfos:
        if ab.name == tableName:
            return ab.fullColumns
    return []


def parseColumns(tmpTableDesc):
    tmpfullColumns = []
    for tl in tmpTableDesc:
        columnInfo = ColumnInfo()
        columnInfo.shortType = getShortTypeMapper(tl[1])
        columnInfo.name = tl[0]
        # appendAttr(columnInfo, "name", str(tl[0]))
        columnInfo.jdbcType = tl[1]
        columnInfo.fullType = getTypeMapper(tl[1])
        columnInfo.null = tl[2]
        columnInfo.primaryKey = tl[3]
        # appendAttr(columnInfo, "primaryKey", str(tl[3]))

        columnInfo.exTra = tl[5]
        tmpfullColumns.append(columnInfo)
    return tmpfullColumns


def parseOtherColumns(fullColumns):
    tmpOtherrColumn = fullColumns.copy()
    for ij in tmpOtherrColumn:
        if "pri" in ij.primaryKey.lower():
            fullColumns.remove(ij)
    return fullColumns


def parsePKColumns(fullColumns):
    tmpPKColumn = fullColumns.copy()
    for jk in tmpPKColumn:
        if "pri" in jk.primaryKey.lower():
            return copy.copy(jk)


def parseForignInfo(b):
    ForignInfos = []

    # print(b)
    if b:
        for ai in b:
            tmpForignInfo = ForeignInfo()
            tmpForignInfo.ownTableName = ai[0]
            tmpForignInfo.ownColumn = ai[1]
            tmpForignInfo.targetTableName = ai[2]
            tmpForignInfo.targetColumn = ai[3]

            # if tmpForignInfo.ownTableName in kk.name:
            #     print("-------------"+kk.name)

            ForignInfos.append(tmpForignInfo)

    return ForignInfos


def appendsNameCaseAttr(tables):
    for a in tables:
        a.appendSelfAttr()
    return tables


def parseJoinTables(tableInfos):
    for aa in tableInfos:
        for bb in range(len(aa.foreignInfos)):
            # print("%s  -> %s " % (aa.foreignInfos[bb].ownTableName, aa.foreignInfos[bb].targetTableName))
            cola = getColumnFromTableInfos(tableInfos, aa.foreignInfos[bb].ownTableName)
            colb = getColumnFromTableInfos(tableInfos, aa.foreignInfos[bb].targetTableName)
            aa.foreignInfos[bb].joinTablesColumns = aa.foreignInfos[bb].joinTablesColumns + cola
            aa.foreignInfos[bb].joinTablesColumns = aa.foreignInfos[bb].joinTablesColumns + colb
            #
            # # print(type(aa.pkColumn))
            # if "TableInfo.ColumnInfo" in str(type(aa.pkColumn)):
            #     aa.pkColumnUpper = copy.copy(aa.pkColumn)
            #     aa.pkColumnUpper.nameUpper = aa.pkColumnUpper.name
            # else:
            #     print("类型不符合，没有设置主键？")
    return tableInfos


class Mapper(object):
    # 映射数据库
    conn = None
    projectConfig = None

    def __init__(self, conn, config):
        self.conn = conn
        self.projectConfig = config

    def getTables(self):
        # 获取所有表名
        results = []
        try:
            with self.conn.cursor() as cursor:
                sql = '''SHOW TABLES'''
                cursor.execute(sql)
                result = cursor.fetchall()
                for i in range(len(result)):
                    results.append(str(result[i][0]))
        finally:
            pass
        return result

    def descTable(self, tableName):
        # 获取所有字段的详情信息
        results = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'DESC %s' % tableName
                cursor.execute(sql)
                result = cursor.fetchall()
                # results.append(tableName)

                if "PRI" not in str(result):
                    print("没有设置主键：%s" % tableName)

                for i in range(len(result)):
                    results.append(result[i])
        finally:
            pass
            # conn.close()
        return results

    def getAllForignKey(self, dataBase, table):
        # 获取与此表所有的关联的表的信息（表名，字段）
        results = []
        # print("表：%s" % table)
        try:
            with self.conn.cursor() as cursor:
                sql = "select TABLE_NAME,COLUMN_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME,CONSTRAINT_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE  where CONSTRAINT_SCHEMA ='%s' AND TABLE_NAME = '%s' and REFERENCED_TABLE_NAME is not null and REFERENCED_COLUMN_NAME is not null and REFERENCED_TABLE_SCHEMA is not null;" % (
                    dataBase, table)
                cursor.execute(sql)
                result = cursor.fetchall()
                for j in range(len(result)):
                    results.append(str(result[j]))
        finally:
            pass

        # if not result:
        # print("%s无外键"%table)
        return result

    def generateSQLByForignKey(self, forign2):
        # 练级查询生成sql
        for i in forign2:
            ownTableName = i[3]
            ownFkName = i[4]
            targetTableName = i[0]
            targetFkName = i[1]
            print('select * from %s,%s where %s.%s = %s.%s' % (
                ownTableName, targetTableName, ownTableName, ownFkName, targetTableName, targetFkName))

    def analyzeTables(self):
        tableNames = self.getTables()
        # 解析表，封装表的信息
        tableInfos = []

        for tableName in tableNames:
            # tmpTable = tmpTable[0]
            tableDescs = self.descTable(tableName)

            tableInfo = TableInfo()
            tableInfo.name = str(tableName[0])
            # appendAttr(tableInfo, "name", str(tmpTable[0]))

            # 表中所有字段
            fullColumns = parseColumns(tableDescs)
            tableInfo.fullColumns = fullColumns

            # 表中非主键的字段(从所有字段中删掉主键字段)
            tableInfo.otherColumns = parseOtherColumns(fullColumns.copy())

            # 表中主键字段(从所有字段获取主键字段)
            tableInfo.pkColumn = parsePKColumns(fullColumns.copy())

            # 获取所有外键引用列表
            b = self.getAllForignKey(self.projectConfig.get("MysqlDb"), tableName[0])
            tableInfo.foreignInfos = parseForignInfo(b)

            # 表结构封装
            tableInfos.append(tableInfo)

        # 反射给Tables所有属性添加xxxxCamelCase的属性，，如name,添加了nameCamelCase
        tableInfos = appendsNameCaseAttr(tableInfos)

        # 最后表信息齐全了， 把具有外键引用的表，两个表的所有字段合并到一起。
        tableInfos = parseJoinTables(tableInfos)

        return tableInfos

    def readDatabaseMaps(self):
        maps = CIMultiDict()
        maps.add("tableInfo", self.analyzeTables())
        return maps
