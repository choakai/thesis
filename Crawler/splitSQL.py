import pyodbc

connStr = 'DRIVER={SQL Server};SERVER=localhost;DATABASE=thesis;UID=sa;PWD=P@ssw0rd'
conn = pyodbc.connect(connStr)

strSQL ="select * from PPT_PoliticMan_201411060151"
cursor = conn.cursor()
cursor.execute(strSQL)

#row = cursor.fetchone()
#if row:
#    print row
for row in cursor:
    print row.context_data2.encode(encoding="utf-8", errors="strict")
