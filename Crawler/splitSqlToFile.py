# -*- coding: utf-8 -*-
#coding=utf-8 
import sys 
import pyodbc
import codecs
import win32com.client
connStr = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=thesis;UID=sa;PWD=P@ssw0rd'
conn = pyodbc.connect(connStr)

FilePath = 'D:\\Crawler\\CKIPClient\\thesis\\in\\'

#conn = win32com.client.Dispatch(r'ADODB.Connection')
#DSN = 'Provider=SQLNCLI11.1;Integrated Security="";Persist Security Info=False;User ID=sa;Password=P@ssw0rd;Initial Catalog=THESIS;Data Source=(local);'
#conn.Open(DSN)

strSQL ="select * from data_src order by urlid"
cursor = conn.cursor()
cursor.execute(strSQL)

#row = cursor.fetchone()
#if row:
#    print row
for row in cursor:
    try:
        
        #print row.context_data
        strContext = unicode(row.context_data)
        
        intFlag = 1
        while len(strContext) > 0:
            if len(strContext) <= 3000:
                f = codecs.open(FilePath + str(row.urlid) +'_'+str(intFlag) + ".txt", "w+", "utf-8")
                f.writelines(unicode(strContext))
                f.close()
                strContext = ''
                continue
            else:
                flag = [0]
                flag[len(flag):] = [strContext[:3000].rfind(u',')]
                flag[len(flag):] = [strContext[:3000].rfind(u'.')]
                flag[len(flag):] = [strContext[:3000].rfind(u'!')]
                flag[len(flag):] = [strContext[:3000].rfind(u'?')]
                flag[len(flag):] = [strContext[:3000].rfind(u'，')]
                flag[len(flag):] = [strContext[:3000].rfind(u'。')]
                flag[len(flag):] = [strContext[:3000].rfind(u'！')]
                flag[len(flag):] = [strContext[:3000].rfind(u'？')]
                maxflag = max(flag)
                if maxflag == 0:
                    break
                f = codecs.open(FilePath + str(row.urlid) +'_'+str(intFlag) + ".txt", "w+", "utf-8")
                
                f.writelines(unicode(strContext[:maxflag]))
                f.close()
                strContext = strContext[maxflag:]
                intFlag += 1
                
    except:
        type, value, tb = sys.exc_info()
        print "Unexpected error:", type
        print "Unexpected error:", value.message
