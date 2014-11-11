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
import base64 
headers = {
    'Referer':'http://www.appledaily.com.tw'
}

homeUrl = 'http://www.appledaily.com.tw/'
#論壇首頁 appledaily 政治
getUrl = 'http://www.appledaily.com.tw/realtimenews/section/politics/'
FilePath = 'd:\\Crawler\\'
#取得最大頁數
intGetMaxPage = 20

fw = lambda f,s: f.write(s)
rl = lambda f: f.readline().strip()
now = datetime.datetime.now()
f = codecs.open(FilePath +"Appledaily_politics" + now.strftime("%Y%m%d%H%M") + ".txt", "w+", "utf-8")

#抓取內容
def getpageContext(soup,page_url):        
    txtReturn = ""
    try:           
        txtTopic = soup.find("h1",{'id':'h1'})
        
        print txtTopic.text
        soup_main = soup.find("article",attrs={"class":re.compile(r"mpatc(\s\w+)?")})
        #txtArticle = kk.find("a",id=True,title=True,href=True)
        #print txtArticle.text
        txtDate = soup.find("time",datetime=True)
        print txtDate.text
        txtContext = soup.find("p",{"id":"summary"},style=True)
        #print txtContext.text
        #f.writelines(page_url + '|||' + txtDate.text + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext.text + "\n")
        txtReturn = page_url + '|||' + txtDate.text + '|||'+ txtTopic.text + '|||' + txtContext.text + "\n"        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        pass
    f.writelines(txtReturn)
    #return txtReturn
        
def main():
    
    #找頁數
    resp = urllib2.urlopen(getUrl + "1",timeout=10)
    soup = BeautifulSoup(resp)
    soup = soup.find("nav",attrs={"class":re.compile(r"page_switch(\s\w+)?")})
    #基本1頁
    intMax = 1
    for intPage in soup.findAll('a' ,href=True,title=True):
        if intMax < intPage.text :
            try:
                intMax = int(intPage.text)
            except:
                continue
    #print intMax

    for p in range(1,intMax +1):
        try:
            resp = urllib2.urlopen(getUrl + str(p),timeout=10)
            soup = BeautifulSoup(resp)

            soup_main = soup.find("div",attrs={"class":re.compile(r"abdominis(\s\w+)?")})

        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "Unexpected error:", sys.exc_info()[1]
            continue
        for k in soup_main.findAll("a", target=True,href=True): # 抓< div class='p=name'>...< /div>
            try:
            
                url = k.get('href') # 各商品URL
                #print url
                url = urllib.quote(url.encode('utf8'))
                resp_text_page = urllib2.urlopen(homeUrl + url, timeout=10)
                soup_text_page = BeautifulSoup(resp_text_page)
                
                getpageContext(soup_text_page,homeUrl + url)
        
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "Unexpected error:", sys.exc_info()[1]
                continue

main()
