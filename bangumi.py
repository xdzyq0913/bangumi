#!/usr/bin/env python 
#coding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re
import sys
reload(sys)   
sys.setdefaultencoding('utf8')  
sys.setrecursionlimit(15000)
address = 'http://bangumi.tv/anime/browser?sort=rank&page='

class Bangumi():
    def GetHtml(self, html):
       req = urllib2.Request(html)
       resp = urllib2.urlopen(req)
       respHtml = resp.read()
       return respHtml

    def FetchInfo(self):
        self.nameResult = []
        self.scoreResult = []
        for page in range(1,125):
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

if __name__ == "__main__":
    bang = Bangumi()
    bang.FetchInfo()
    f = open("./bangumiData.txt",'w+')
    for i in range(0,len(bang.nameResult)):
       print >>f,"%s %s" % (bang.nameResult[i],bang.scoreResult[i])
    f.close()
