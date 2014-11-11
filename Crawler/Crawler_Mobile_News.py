# -*- coding: utf-8 -*-
#coding=utf-8 
import sys
import urllib
import urllib2
import codecs
import re
import math
import datetime
from BeautifulSoup import BeautifulSoup
#from bs4 import BeautifulSoup
headers = {
    'Referer':'http://www.mobile01.com'
}

homeUrl = 'http://www.mobile01.com/'
#論壇首頁 Mobile01 首頁 » 生活娛樂 » 新聞與時事
getUrl = 'http://www.mobile01.com/topiclist.php?f=638'
FilePath = 'd:\\Crawler\\'
#取得最大頁數
intGetMaxPage = 20


fw = lambda f,s: f.write(s)
rl = lambda f: f.readline().strip()
now = datetime.datetime.now()
f = codecs.open(FilePath +"Mobile01_" + now.strftime("%Y%m%d%H%M") + ".txt", "w+", "utf-8")

#抓取內容
def getpageContext(soup,page_url):        
    txtTopic = soup.find("h1",{'class':'topic'})
    txtReturn = ""
    print txtTopic.text

    soup_main = soup.find("main")
    for kk in soup_main.findAll("article"):  
        try:           
            txtArticle = kk.find("a",id=True,title=True,href=True)
            #print txtArticle.text
            txtDate = kk.find("div",{'class':'date'})
            print txtDate.text
            txtContext = kk.find("div",id=True)
            #print txtContext.text
            #f.writelines(page_url + '|||' + txtDate.text + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext.text + "\n")
            txtX = page_url + '|||' + txtDate.text + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext.text + "\n"
            txtReturn += txtX
        except:
            print "Unexpected error:", sys.exc_info()[0]
            continue
    return txtReturn



#取得文章頁數
def contextPageUrl(soup,page_url):
    txtTopic = ""
    for page in soup.findAll("div",{'class':'pagination'}):
        txtTopic =page

    print txtTopic.text
    #基本1頁
    intMax = 1
    for intPage in txtTopic.findAll('a' ,href=True):
        if intMax < intPage.text :
            try:
                intMax = int(intPage.text)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                continue
    print intMax
    txtSubContext = ""
    for i in range(1,intMax+1):
        try:
        
            resp = urllib2.urlopen(page_url + '&p=' + str(i), timeout=10)
            realsock = resp.fp._sock.fp._sock
            soup = BeautifulSoup(resp)
            txtWrite = getpageContext(soup,page_url + '&p=' + str(i))
            f.writelines(txtWrite)
            realsock.close() 
            resp.close()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            continue
    #return txtSubContext

def main():
    for p in range(1,intGetMaxPage +1):
        try:
            resp = urllib2.urlopen(getUrl + 'p=' + str(p),timeout=10)
            soup = BeautifulSoup(resp)
        except:
            continue
        #for k in soup.findAll("div", {'class': 'p-name'}): # 抓< div class='p=name'>...< /div>
        for k in soup.findAll("span", {'class': 'subject-text'}): # 抓< div class='p=name'>...< /div>
            try:
            
                url = k.a.get('href') # 各商品URL
                #print url
        
                page_url = homeUrl + url
                #print page_url
                resp_text_page = urllib2.urlopen(homeUrl + url, timeout=10)
            
                soup_text_page = BeautifulSoup(resp_text_page)
                contextPageUrl(soup_text_page,page_url)    
            except:
                print "Unexpected error:", sys.exc_info()[0]
                continue

main()