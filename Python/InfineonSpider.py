import urllib2
import re

def downloadPartNumber(productPageURL):
     res = urllib2.urlopen(productPageURL)
     page = res.read()

     filt = re.compile(r'onclick="window.open\(this\.href\); return false;">.+</a>&nbsp;')
     filt2 = re.compile(r'onclick="window.open\(this\.href\); return false;">(.+)</a>&nbsp;')
     filt3 = re.compile(r'<meta name="title" content="(.+)" />')

     result = filt.findall(page)
     family = filt3.search(page).group(1)
     print family

     resultString = ''
     for i in range(len(result)):
          partnumber =  filt2.search(result[i])
          result[i] = partnumber.group(1)
          #print result[i]
          resultString  = resultString + result[i] + '\t' +family + '\n'

     print resultString
     fileName = 'Part Number.txt'
     f = open('Part Number.txt', 'a')
     f.write(resultString)
     f.close()

categoryList = {
                'Power'  :   'http://www.infineon.com/cms/en/product/power/channel.html?channel=db3a304319c6f18c011a154646852706',
                'Automotive System IC'  :    'http://www.infineon.com/cms/en/product/automotive-system-ic/channel.html?channel=db3a304319c6f18c011a1524811d26bf',
                'ESD & EMI'   :    'http://www.infineon.com/cms/en/product/esd-and-emi/channel.html?channel=ff80808112ab681d0112ab6b18820716',
                'Microcontroller'  :    'http://www.infineon.com/cms/en/product/microcontroller/channel.html?channel=ff80808112ab681d0112ab6b2dfc0756',
                'RF & Wireless Control' :  'http://www.infineon.com/cms/en/product/rf-and-wireless-control/channel.html?channel=db3a304319c6f18c011a14e8eb3225fe',
                'Security IC' :    'http://www.infineon.com/cms/en/product/security-ic/channel.html?channel=db3a30433fa9412f013fc3547ddf1e8e',
                'Sensor IC'   :    'http://www.infineon.com/cms/en/product/sensor-ics/channel.html?channel=ff80808112ab681d0112ab68eaf1008b',
                'Smart Card IC'    :    'http://www.infineon.com/cms/en/product/smart-card-ic/channel.html?channel=ff80808112ab681d0112ab6923e10125',
                'Transceiver' :    'http://www.infineon.com/cms/en/product/transceiver/channel.html?channel=db3a3043442f82090144305a607e024f',
                'Transistor & Diode'    :    'http://www.infineon.com/cms/en/product/transistor-and-diode/channel.html?channel=db3a304319c6f18c011a14e6b8e025f7'
               }

url = 'http://www.infineon.com/cms/en/product/power/channel.html?channel=db3a304319c6f18c011a154646852706'
page = urllib2.urlopen(url).read()
filt = re.compile(r'<div\s+id="content\-zone">(.+)</div>')
result = filt.search(page)
print result

