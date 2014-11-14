import sys
import os
import codecs

FilePath = 'D:\\Crawler\\CKIPClient\\thesis\\out\\'
TargetPath = 'D:\\Crawler\\CKIPClient\\thesis\\'
fTargetFile = codecs.open(TargetPath + "target" + ".txt", "w+", "utf-8")
for root, dirs, files in os.walk(FilePath):
    print root
    for f in files:
        print os.path.join(root, f)        

        ff = codecs.open(os.path.join(root, f), encoding='utf-8')
        for line in ff:
            #去除大寫空白
            line = line.replace(u'\u3000','')
            strLine = line.strip().split(')')
            intSeq = 1
            
            for yy in strLine:
                try:
                    
                    yy = yy.replace(' ','')
                    yy = yy.replace(u'\u3000','')
                    
                    if len(yy) == 0:
                        continue
                    xx = yy.split('(')
                    fileName = f.split('.')
                    urlid = fileName[0].split('_')[0]
                    
                    #print intSeq
                    #print xx[0]
                    #print xx[1]
                    intSeq += 1
                    txtLine = "%s|||%s|||%s|||%s|||%s\n" %(urlid,fileName[0].split('_')[1],str(intSeq),xx[0],xx[1])
                    fTargetFile.writelines(txtLine)
                except:
                    type, value, tb = sys.exc_info()
                    print value.message
                    pass

fTargetFile.close()