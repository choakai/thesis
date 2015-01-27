# -*- coding: utf-8 -*-
#-----coding=utf-8 
# coding=cp950
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import codecs
import re
import math
import time 
import datetime
import pyodbc
import win32com.client
import sys
import os
import codecs
import linecache

from BeautifulSoup import BeautifulSoup
#from bs4 import BeautifulSoup
headers = {
    'Referer':'https://www.ptt.cc/'
}

homeUrl = 'https://www.ptt.cc/'
#您現在的位置是 PoliticMan - 政黨/政治人物研究院 的看板 
getUrl = 'https://www.ptt.cc/bbs/5062.html'
FilePath = 'D:\\Crawler\\target_url\\'
FilePath_Target = 'D:\\Crawler\\target_data\\'
# 
connStr = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=url_src;UID=sa;PWD=P@ssw0rd'
connStr_sis = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=THESIS;UID=sa;PWD=P@ssw0rd'
connStr_ado = 'Provider=SQLNCLI11.1;Data Source=(local);Initial Catalog=url_src;User ID=sa;Password=P@ssw0rd;' #%('','url_src' ,'sa', 'P@ssw0rd')
connStr_ado = 'Provider=SQLNCLI11.1;Persist Security Info=False;User ID=sa;Password=P@ssw0rd;Initial Catalog=THESIS;Data Source=(local);'
#取得最大頁數
#intGetMaxPage = 20

fw = lambda f,s: f.write(s)
rl = lambda f: f.readline().strip()
now = datetime.datetime.now()

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)



#抓取內容
def getpageContext(soup,page_url):        
    print page_url
    start = time.time()

    txtReturn = ""

    soup_main = soup.find("div",{'id':'main-content'})

    try:
        soup_main = soup.find("div",{'id':'main-content'})
        
        txtArticle = soup_main.find("span",{'class':'article-meta-value'})
        #print txtArticle.text
        soup_main.div.extract() #delete Article
        soup_main.div.extract() #delete board

        txtTopic = soup_main.find("span",{'class':'article-meta-value'})
        #print txtTopic.text.encode("utf-8", "replace") 
        soup_main.div.extract() #delete topic

        txtDate = soup_main.find("span",{'class':'article-meta-value'})
        #print txtDate.text  #delete date

        dt = datetime.datetime.strptime(txtDate.text ,'%a %b %d %H:%M:%S %Y')

        soup_main.div.extract()
        
        try:
            while(1==1):
                soup_main.span.extract()
        except:
            pass

        txtContext = soup_main.text
        txtContext = "".join(txtContext.split())
        
        txtX = page_url + '|||' + dt.strftime('%Y%m%d%H%M%S') + '|||'+ txtTopic.text + '|||' + txtArticle.text + '|||' + txtContext + "\n"
            
        txtReturn += txtX

        end = time.time()
        elapsed = end - start
        print "Time taken: ", elapsed, "seconds."
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        PrintException()
        
        pass
    return txtReturn
   
def main():
    #python dont know windows's cp65001 = utf-8 
    try:
        codecs.lookup('cp65001')
    except:
        def cp65001(name):
            if name.lower() == 'cp65001':
                return codecs.lookup('utf-8')
        codecs.register(cp65001)

    try:
        i = 0 
        for root, dirs, files in os.walk(FilePath):
            #print root
            filename = ""
            for fff in files:

                print os.path.join(root, fff) 
                ff = codecs.open(os.path.join(root, fff), encoding='utf-16')
                for line in ff:
                    try:
                        i = i + 1
                        print i
                        f = codecs.open(FilePath_Target +"PPT_PoliticMan_" + now.strftime("%Y%m%d%H%M") + "_" + str( os.getpid() )+ ".txt", "w+", "utf-8")
                        page_url = line.rstrip()
                        resp = urllib2.urlopen(page_url , timeout=10)
                        soup = BeautifulSoup(resp)
                        txtWrite = getpageContext(soup,page_url)
                        f.writelines(txtWrite)
                        resp.close()
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        print "Unexpected error:", sys.exc_info()[1]
                        PrintException()
                        pass
                ff.close()
                #delete file 
                try:
                    filename = os.path.join(root, fff)    
                    if os.path.isfile(filename):
                        os.remove(filename)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print "Unexpected error:", sys.exc_info()[1]
                    PrintException()
                    pass
        
    except:
        #continue
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        PrintException()
        pass

main()
