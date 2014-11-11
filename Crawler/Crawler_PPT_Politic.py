# -*- coding: utf-8 -*-
#-----coding=utf-8 
# coding=cp950
import sys
import urllib
import urllib2
import codecs
import re
import math
import time 
import datetime
import pyodbc
import win32com.client
from BeautifulSoup import BeautifulSoup
#from bs4 import BeautifulSoup
headers = {
    'Referer':'https://www.ptt.cc/'
}

homeUrl = 'https://www.ptt.cc/'
#您現在的位置是 PoliticMan - 政黨/政治人物研究院 的看板 
getUrl = 'https://www.ptt.cc/bbs/5062.html'
FilePath = 'D:\\Crawler\\'
# 
connStr = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=url_src;UID=sa;PWD=P@ssw0rd'
connStr_sis = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=THESIS;UID=sa;PWD=P@ssw0rd'
connStr_ado = 'Provider=SQLNCLI11.1;Data Source=(local);Initial Catalog=url_src;User ID=sa;Password=P@ssw0rd;' #%('','url_src' ,'sa', 'P@ssw0rd')
#取得最大頁數
#intGetMaxPage = 20


fw = lambda f,s: f.write(s)
rl = lambda f: f.readline().strip()
now = datetime.datetime.now()
f = codecs.open(FilePath +"PPT_PoliticMan_" + now.strftime("%Y%m%d%H%M") + ".txt", "w+", "utf-8")

#抓取內容
def getpageContext(soup,page_url):        
    
    txtReturn = ""
    #print txtTopic.text

    soup_main = soup.find("div",{'id':'main-content'})

    #print soup_main.text

    try:
        soup_main = soup.find("div",{'id':'main-content'})
        
        #soup_main.div.contents[2].extract()
        #soup_main.div.contents[1].extract()
        #soup_main.div.contents[0].extract()

        txtArticle = soup_main.find("span",{'class':'article-meta-value'})
        print txtArticle.text
        soup_main.div.extract() #delete Article
        soup_main.div.extract() #delete board

        txtTopic = soup_main.find("span",{'class':'article-meta-value'})
        print txtTopic.text
        soup_main.div.extract() #delete topic

        txtDate = soup_main.find("span",{'class':'article-meta-value'})
        print txtDate.text  #delete date

        dt = datetime.datetime.strptime(txtDate.text ,'%a %b %d %H:%M:%S %Y')

        soup_main.div.extract()
        
        try:
            while(1==1):
                soup_main.span.extract()
        except:
            pass


        txtContext = soup_main.text
        txtContext = "".join(txtContext.split())
        print txtContext
        #f.writelines(page_url + '|||' + txtDate.text + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext.text + "\n")
        txtX = page_url + '|||' + dt.strftime('%Y%m%d%H%M%S') + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext + "\n"

        conn_ado = win32com.client.Dispatch(r'ADODB.Connection') 

        conn_ado.open(connStr_ado)




        conn = pyodbc.connect(connStr)
        strSQL ="insert into url_src..url (url) values (?)"
        cursor = conn.cursor()
        cnt = cursor.execute(strSQL ,page_url).rowcount
        cursor.commit() 
        if cnt > 0 :
            strSQL ="select urlid from url_src..url where url= ? "
            cursor = conn.cursor()
            urlid = cursor.execute(strSQL ,page_url).fetchone()[0]

            conn_sis = pyodbc.connect(connStr_sis)            

            strSQL ="insert into thesis..data_src ( urlid ,url_date ,topic ,author ,context_data) values (?,?,?,?,?)"
            #strSQL ="insert into thesis..data_src ( urlid ) values ("+ str(urlid) +")"
            cursor = conn_sis.cursor()
            cnt = cursor.execute(strSQL ,urlid,dt.strftime('%Y%m%d%H%M%S') ,txtTopic.text ,txtArticle.text , txtContext ).rowcount
            #cnt = cursor.execute(strSQL  ).rowcount
            cursor.commit() 
            conn_sis.close()
            conn.close()
            
        txtReturn += txtX
    except:
        print "Unexpected error:", sys.exc_info()[0]
        txt = sys.exc_info()[1].str()
        print "Unexpected error:", txt
        pass
    return txtReturn

#取得文章頁數
def contextPageUrl(soup,page_url):
    soup_src = soup
    txtTopic = ""
    #r-list-container bbs-screen
    soup_main = soup.find("div",attrs={"class":re.compile(r"r-list-container(\s\w+)?")})
    
    txtSubContext = ""
    for k in soup_main.findAll('a', href=True):      
        try:
            url = k.get('href')
            page_url = homeUrl + url

            # viery url 

            conn_ado = win32com.client.Dispatch(r'ADODB.Connection') 
            conn_ado.open(connStr_ado)


            conn = pyodbc.connect(connStr)
            strSQL ="select count(*) from url where url = ? "
            cursor = conn.cursor()
            count = cursor.execute(strSQL ,page_url).fetchone()[0]

            if count > 0 :
                conn.close()
                continue

            resp = urllib2.urlopen(page_url , timeout=10)
            realsock = resp.fp._sock.fp._sock
            soup = BeautifulSoup(resp)
            
            txtWrite = getpageContext(soup,page_url)
            f.writelines(txtWrite)
            realsock.close() 
            resp.close()
            conn.close()
        except:
            type, value, tb = sys.exc_info()
            print "Unexpected error:", type
            print "Unexpected error:", value.message
            continue
        #else:
            


    try:
        soup_bar = soup_src.find("div",{"class":"action-bar"})
        soup_bar.div.extract()
    
        ##soup.find("div",{"class":re.compile(r"btn-group(\s\w+)?")}).extract()
        
        soup_btn =  soup_bar.find("div")
        soup_btn.a.extract() #delete 
            
        print soup_btn.a.get('href')
        url = soup_btn.a.get('href')
        page_url = homeUrl + url
        resp = urllib2.urlopen(page_url , timeout=10)
        soup = BeautifulSoup(resp)
        contextPageUrl(soup,page_url)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        pass
    
def main():

    #for p in range(1,intGetMaxPage +1):
    #soup = BeautifulSoup()
    try:
        resp = urllib2.urlopen(getUrl,timeout=10)
        soup = BeautifulSoup(resp)
        soup = soup.find('div' ,{'id':'prodlist'})

    
        #for k in soup.findAll("div", {'class': 'p-name'}): # 抓< div class='p=name'>...< /div>
        for k in soup.findAll('a', href=True): 
            try:
            
                url = k.get('href') 
                print k.text
                print url 
        
                page_url = homeUrl + url
                print page_url
                resp_text_page = urllib2.urlopen(homeUrl + url, timeout=10)
            
                soup_text_page = BeautifulSoup(resp_text_page)
                contextPageUrl(soup_text_page,page_url)    
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "Unexpected error:", sys.exc_info()[1]
                continue
    except:
        #continue
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        pass

main()
