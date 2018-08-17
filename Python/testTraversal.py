import os
import time

result = os.walk("G:\Project Documents\Corp_Autoliv_Lib Translation\source library 021218\SymbolLibs\Imported Libraries.PrjPcb")
for root, dirs, files in result:
     for fileName in files:
          fullName = root + '\\' + fileName
          fileSize = os.path.getsize(fullName)
          modifyDate = time.ctime(os.stat(fullName).st_mtime)
          if ".Schlib" in fullName:
##               print fullName + "^" + str(fileSize)
               print fileName + "^" + modifyDate
     break;
