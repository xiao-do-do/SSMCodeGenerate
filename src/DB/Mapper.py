import copy
import re

from multidict import CIMultiDict
from db.TableInfo import TableInfo, ColumnInfo, ForignInfo
from utils import ConfigReader
from utils.Utils import *


def getTypeMapper(mapType):
    # 从config.ini中寻找与数据库相匹配的JAVA数据类型
    typeMapper = ConfigReader.getTypeMapperConfig()
    for i in typeMapper:
        if r"\(" in i:
            pattern = re.compile(i)  # 查找数字
            result1 = pattern.findall(mapType)
            if result1:
                # print("------%s %s" % (i, typeMapper[i]))
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


def getColumnFromTableInfos(listTableInfos, tableName):
    for ab in listTableInfos:
        if ab.name == tableName:
            return ab.fullColumn
    return []


def parseColumns(listTmpTableDesc):
    tmpfullColumns = []
    for tl in listTmpTableDesc:
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
            tmpForignInfo = ForignInfo()
            tmpForignInfo.ownTableName = ai[0]
            tmpForignInfo.ownColumn = ai[1]
            tmpForignInfo.targetTableName = ai[2]
            tmpForignInfo.targetColumn = ai[3]

            # if tmpForignInfo.ownTableName in kk.name:
            #     print("-------------"+kk.name)

            ForignInfos.append(tmpForignInfo)

    return ForignInfos


def appendsCamelCaseAttr(listTables):
    for a in listTables:
        a.appendSelfAttr()
    return listTables





def parseJoinTables(listTableInfo):
    for aa in listTableInfo:
        for bb in range(len(aa.foreignInfo)):
            # print("%s  -> %s " % (aa.foreignInfo[bb].ownTableName, aa.foreignInfo[bb].targetTableName))
            cola = getColumnFromTableInfos(listTableInfo, aa.foreignInfo[bb].ownTableName)
            colb = getColumnFromTableInfos(listTableInfo, aa.foreignInfo[bb].targetTableName)
            aa.foreignInfo[bb].joinTablesColumn = aa.foreignInfo[bb].joinTablesColumn + cola
            aa.foreignInfo[bb].joinTablesColumn = aa.foreignInfo[bb].joinTablesColumn + colb


            #
            # # print(type(aa.pkColumn))
            # if "TableInfo.ColumnInfo" in str(type(aa.pkColumn)):
            #     aa.pkColumnUpper = copy.copy(aa.pkColumn)
            #     aa.pkColumnUpper.nameUpper = aa.pkColumnUpper.name
            # else:
            #     print("类型不符合，没有设置主键？")
    return listTableInfo


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
                    # results.append(result[i][0])
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
            targenFkName = i[1]
            print('select * from %s,%s where %s.%s = %s.%s' % (
                ownTableName, targetTableName, ownTableName, ownFkName, targetTableName, targenFkName))

    def analyzeTables(self):
        tables = self.getTables()
        # 解析表，封装表的信息
        listTableInfo = []

        for tmpTable in tables:
            # tmpTable = tmpTable[0]
            listTmpTableDesc = self.descTable(tmpTable)

            tableInfo = TableInfo()
            tableInfo.name = str(tmpTable[0])
            # appendAttr(tableInfo, "name", str(tmpTable[0]))

            # 表中所有字段
            fullColumns = parseColumns(listTmpTableDesc)
            tableInfo.fullColumn = fullColumns

            # 表中非主键的字段(从所有字段中删掉主键字段)
            tableInfo.otherColumn = parseOtherColumns(fullColumns.copy())

            # 表中主键字段(从所有字段获取主键字段)
            tableInfo.pkColumn = parsePKColumns(fullColumns.copy())

            # 获取所有外键引用列表
            b = self.getAllForignKey(self.projectConfig.get("MysqlDb"), tmpTable[0])
            tableInfo.foreignInfo = parseForignInfo(b)

            # 表结构封装
            listTableInfo.append(tableInfo)


        # 反射给Tables所有属性添加xxxxCamelCase的属性，，如name,添加了nameCamelCase
        listTableInfo = appendsCamelCaseAttr(listTableInfo)

        # 最后表信息齐全了， 把具有外键引用的表，两个表的所有字段合并到一起。
        listTableInfo = parseJoinTables(listTableInfo)





        return listTableInfo

    def readDatabaseMaps(self):
        maps = CIMultiDict()
        maps.add("tableInfo", self.analyzeTables())
        return maps
