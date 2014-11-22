import tempfile, time, subprocess,os
import shutil

CKIPath = 'D:\\Crawler\\CKIPClient\\'
CraSourcePath = 'D:\\Crawler\\CKIPClient\\thesis2\\in\\'

for root, dirs, files in os.walk(CraSourcePath):
    for f in files:
        try:
            print os.path.join(root, f)
            fileX = str(os.path.join(root, f))
            shutil.move( os.path.join(root, f) ,fileX.replace('\\in\\','\\cur\\'))
        
            p = subprocess.call(['java', '-jar', CKIPath +'CKIPClient.jar' , CKIPath + 'ckipsocket-utf-8.propeties', CraSourcePath.replace('\\in\\','\\cur\\') ,CraSourcePath.replace('\\in\\','\\out\\')])

            print p
            if p == 0 :
                shutil.move( fileX.replace('\\in\\','\\cur\\') ,fileX.replace('\\in\\','\\finish\\'))
        except:
            type, value, tb = sys.exc_info()
            print "Unexpected error:", type
            print "Unexpected error:", value.message