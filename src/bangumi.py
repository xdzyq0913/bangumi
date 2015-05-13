#!/usr/bin/env python 
#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import sqlite3

reload(sys)   
sys.setdefaultencoding('utf8')  
sys.setrecursionlimit(15000)
address = 'http://bangumi.tv/anime/browser?sort=rank&page='

class DataBase():
    def __init__(self):
        self.cx = sqlite3.connect("../db/rank.db")
        self.cu = self.cx.cursor()
        self.cu.execute("create table BangumiRank (id integer primary key, name varchar(50),score float)")
    
    def Insert(self,id,name,score):
        sql = 'insert into BangumiRank values(%d,"%s",%f)' % (id, name, score)
        self.cu.execute(sql)
        self.cx.commit()


class Bangumi():
    def GetHtml(self, html):
       req = urllib2.Request(html)
       resp = urllib2.urlopen(req)
       respHtml = resp.read()
       return respHtml

    def FetchInfo(self):
        self.nameResult = []
        self.scoreResult = []
        for page in range(1,2):
           html = self.GetHtml(address + str(page))
           soup = BeautifulSoup(html)
           nameQuery = soup.find_all(name = "a", attrs={"class":"l","href":re.compile(r'/sub.*')})
           scoreQuery = soup.find_all(name = "small",attrs={"class":"fade"})
           if (len(nameQuery) == 0 ):
              break
           length = len(nameQuery)         
           for i in range(0,length):
              self.nameResult.append(nameQuery[i].string)
              self.scoreResult.append(scoreQuery[i].string)
           nameQuery = []
           scoreQuery = []
    
    def WriteToDataBase(self):
        data = DataBase()
        for i in range(0,len(self.nameResult)):
            data.Insert(i + 1, self.nameResult[i], float(self.scoreResult[i]))


if __name__ == "__main__":
    bang = Bangumi()
    bang.FetchInfo()
    bang.WriteToDataBase()

