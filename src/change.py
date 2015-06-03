#coding:utf-8
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


cx = sqlite3.connect("../db/rank.db")
cu = cx.cursor()

def GetTables():
    table = []
    cu.execute("select name from sqlite_master where type='table'")
    r = cu.fetchall()
    for name in r:
       table.append(name[0])
    return table

def GetNewOnes():
    table = GetTables()
    if len(table) < 2:
        print 'no enough tables'
        return
    leftOne = table[len(table) - 1]
    rightOne = table[len(table) - 2]
    sql = 'select a.name from %s a left join %s b on a.name = b.name where b.rank is null' %(leftOne, rightOne)
    cu.execute(sql)
    r = cu.fetchall()
    if len(r) == 0:
        print 'no new ones'
        return
    for name in r:
        print name[0]
if __name__ == '__main__':
    GetNewOnes()

