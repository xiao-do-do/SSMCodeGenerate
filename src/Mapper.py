import copy
import re

from multidict import CIMultiDict
from TableInfo import TableInfo, ColumnInfo, ForignInfo
from helper import ConfigHelper
from utils import *


# 从config.ini中寻找与数据库相匹配的JAVA数据类型
def getTypeMapper(mapType):
    typeMapper = ConfigHelper.getConfigerItems("typeMapper")
    for i in typeMapper:
        if "\(" in i:
            pattern = re.compile(i)  # 查找数字
            result1 = pattern.findall(mapType)
            if result1:
                # print("------%s %s" % (i, typeMapper[i]))
                return typeMapper[i]
        else:
            if i == mapType:
                return typeMapper[i]
        pass


# 把数据库的所有表映射成一个对象
class Mapper(object):
    conn = None
    projectConfig = None

    def __init__(self, conn, config):
        self.conn = conn
        self.projectConfig = config

    # 获取所有表名
    def getTables(self):
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

    # 获取所有字段的详情信息
    def descTable(self, tableName):
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

    # 获取与此表所有的关联的表的信息（表名，字段）
    def getAllForignKey(self, dataBase, table):
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

    def generateSQLByForignKey(forign2):
        for i in forign2:
            ownTableName = i[3]
            ownFkName = i[4]
            targetTableName = i[0]
            targenFkName = i[1]
            print('select * from %s,%s where %s.%s = %s.%s' % (
                ownTableName, targetTableName, ownTableName, ownFkName, targetTableName, targenFkName))

    def getShortTypeMapper(self, mapType):
        stra = getTypeMapper(mapType)
        if stra:
            cnt = str(stra).rfind(".")
            return stra[cnt + 1:]

    def analyzeTables(self, tables):
        listTableInfo = []

        for tmpTable in tables:
            ForignInfos = []
            # tmpTable = tmpTable[0]
            listTmpTableDesc = self.descTable(tmpTable)

            tableInfo = TableInfo()
            tableInfo.name = str(tmpTable[0])

            # 所有字段的封装
            fullColumns = []
            for tl in listTmpTableDesc:
                columnInfo = ColumnInfo()
                columnInfo.shortType = self.getShortTypeMapper(tl[1])
                columnInfo.name = tl[0]
                columnInfo.fullType = getTypeMapper(tl[1])
                columnInfo.null = tl[2]
                columnInfo.primaryKey = tl[3]
                columnInfo.exTra = tl[5]
                fullColumns.append(columnInfo)

                # print(type)
            # print(type)

            # tableInfo.type = self.getTypeMapper(l[1])
            # tableInfo.shortType = shortType
            tableInfo.fullColumn = fullColumns.copy()

            # 从所有的字段里筛选出逐渐列表
            tableInfo.otherrColumn = fullColumns.copy()
            tmpOtherrColumn = tableInfo.otherrColumn.copy()
            for ij in tmpOtherrColumn:
                if "pri" in ij.primaryKey.lower():
                    tableInfo.otherrColumn.remove(ij)

            # 从所有的字段里筛选出非主键列表
            tableInfo.pkColumn = fullColumns.copy()
            tmpPKColumn = tableInfo.pkColumn.copy()
            for jk in tmpPKColumn:
                if "pri" in jk.primaryKey.lower():
                    tableInfo.pkColumn = copy.copy(jk)

            # 获取所有外键引用列表
            b = self.getAllForignKey(self.projectConfig.get("MysqlDb"), tmpTable[0])
            print(b)
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

            tableInfo.forignInfo = ForignInfos

            # 表结构封装
            listTableInfo.append(tableInfo)

        # for aa in listTableInfo:
        #     for bb in aa.forignInfo:
        #         print(
        #             "%s %s %s -> %s %s" % (aa.name, bb.ownTableName, bb.ownColumn, bb.targetTableName, bb.targetColumn))
        # ForignInfo对象加入外键关联的两个表的字段

        # for jj in ForignInfos:
        #     print("%s -- %s" % (jj.ownTableName, jj.targetTableName))
        # if listTableInfo

        for aa in listTableInfo:
            for bb in range(len(aa.forignInfo)):
                print("%s  -> %s " % (aa.forignInfo[bb].ownTableName, aa.forignInfo[bb].targetTableName))
                cola = self.getColumnFromTableInfos(listTableInfo, aa.forignInfo[bb].ownTableName)
                colb = self.getColumnFromTableInfos(listTableInfo, aa.forignInfo[bb].targetTableName)
                aa.forignInfo[bb].joinTablesColumn = aa.forignInfo[bb].joinTablesColumn + cola
                aa.forignInfo[bb].joinTablesColumn = aa.forignInfo[bb].joinTablesColumn + colb

                aa.nameUpper = CamelCase(aa.name)

                print(type(aa.pkColumn))
                if "TableInfo.ColumnInfo" in str(type(aa.pkColumn)):
                    aa.pkColumnUpper = copy.copy(aa.pkColumn)
                    aa.pkColumnUpper.nameUpper = aa.pkColumnUpper.name
                else:
                    print("类型不符合，没有设置主键？")

                # print(aa.forignInfo[bb].joinTablesColumn)
        return listTableInfo
        pass

    def getColumnFromTableInfos(self, listTableInfos, tableName):
        for ab in listTableInfos:
            if ab.name == tableName:
                return ab.fullColumn
        return []

    def getSqlMaps(self):
        tables = self.getTables()
        maps = CIMultiDict()
        maps.add("listTables", tables)
        # print(maps)

        listTablesDesc = []
        for i in tables:
            i = i[0]
            a = self.descTable(i)
            listTablesDesc.append(a)

        maps.add("listDesc", listTablesDesc)

        # forign2 = getAllForignKey(mysqlDb, tables[0][0])

        # generateSQLByForignKey(forign2)

        # print(listForignKey)
        # maps.add("ForignInfos", self.analyzeForigns(tables))

        #     generateSQLByForignKey(forignList)
        #     print()
        #

        maps.add("tableInfo", self.analyzeTables(tables))

        return maps
