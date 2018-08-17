import urllib2
import re
import string

def downloadPage(url):
     for i in range(len(url)):
          sName =  string.zfill(i,5) + '.html'
          print 'downloading' + str(i) + 'th page'
          f = open(sName,'w+')
          m = urllib2.urlopen(url[i]).read()
          f.write(m)
          f.close()

res = urllib2.urlopen('http://sebug.net/paper/python/index.html')
fi = res.read().decode('gbk')

label = re.compile(r'<dt>.+</dt>')
label2 = re.compile(r'<a\s+href')
label3 = re.compile(r'<a\s+href="(.+)">(.+)</a>')

temp = label.findall(fi)
                    
result = []
for i in range(len(temp)):
     if label2.search(temp[i]):
          result.append(temp[i])


urlTable = []
for i in range(len(result)):
     urlTable.append(label3.search(result[i]).group(1))
     urlTable[i] = 'http://sebug.net/paper/python/' + urlTable[i]
                    

downloadPage(urlTable)





