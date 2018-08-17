import urllib2
import urllib
import re

cookies = "WBmain_flyout-products-webench=0; WBmain_flyout-tools-webench=0; AP_COOKIE_EN=computerId-C_EN_159133348&geoStateCode-TX&ipGeoMapDate-1395992429054&expiryDate-1432371308376&lastVisitedDate-1400835308376&geoRegion-Americas&createdDate-1368502838324&geoCountryCode-US&ipAddress-23.215.15.27&; AB_TECHDOC_EN=%40DWV00008A%20DWV%20%5ER-PDSO-G8%24%204218796%20%5ERev.%20B%24%7CEN%7C%20_MPDS382%7CPDF%7C0%7C1400835308393%40RGA%20%5ES-PQFP-N20%24%204202802%20%5ERev.%20B%24%7CEN%7C%20_MPQF110%7CPDF%7C0%7C1400830559388%40Infrared%20Thermopile%20Sensor%20in%20Chip-Scale%20Package%20%5ERev.%20C%24%7CEN%7Ctmp006_SBOS518%7C%7C0%7C1397711628851%40Design%20Summary%20for%20WCSP%20Little%20Logic%20%5ERev.%20B%24%7CEN%7C%20_SCET007%7CPDF%7C0%7C1397108827456%40LM5017%20100V%2C600mA%20Constant%20On-Time%20Synchronous%20Buck.%20%5ERev.%20G%24%7CEN%7Clm5017_SNVS783%7C%7C0%7C1396232601509%40PMP8363%20SEC%20PCB%7CEN%7C%20_SLUUA39%7CPDF%7C0%7C1395989520137%40PMP8363%20PRI%20BOM%7CEN%7C%20_SLUR971%7CPDF%7C0%7C1395989515834%40PMP8363%20PRI%20Schematic%7CEN%7C%20_SLUR972%7CPDF%7C0%7C1395989486167%40PMP8363%20SEC%20BOM%7CEN%7C%20_SLUR973%7CPDF%7C0%7C1395989470478%40PMP8363%20SEC%20Schematic%7CEN%7C%20_SLUR974%7CPDF%7C0%7C1395989447858; userType=Anonymous; s_fid=5C98F54B7E68B374-2B679A61CC2DAADE; CID=computerId-C_EN_159133348; __qca=P0-1711364685-1395989377405; WBmain_tab-products-webench=0; WBmain_tab-tools-webench=0; PROMO_TRACKER_EN=SBOS518_3_en_3_1; AB_SEARCH_EN=%40packaging%7Cen%7C0%7C1402476232128%40package%7Cen%7C0%7C1402476221895%40PMP7798%7Cen%7C0%7C1395992474596%40PMP8363%7Cen%7C0%7C1395989425244; optimizelySegments=%7B%22381552649%22%3A%22false%22%2C%22383450955%22%3A%22ie%22%2C%22384220756%22%3A%22referral%22%7D; optimizelyEndUserId=oeu1395989427448r0.9027810097196962; optimizelyBuckets=%7B%7D; REMBR549=uid%3Dx0219966%7Csecuritylevel%3D1; iatc=1; iPlanetDirectoryPro=AQIC5wM2LY4SfcwcR6W3+znj6X0KN9pPfOlnYb4VO0cCF4Y=@AAJTSwAKMTI3MDg4ODE5NgACU0kAAjAzAAJTMQACMDI=#; TIJES5lbcookie=01; TIJES5Login=AQIC5wM2LY4SfczllOXsNERzghZxhIGDLpxVjzFSGbHUxoU%3D%40AAJTSwAKMTQzODE5NTM2NgACU0kAAjAzAAJTMQACMDE%3D%23; TIPASSID=permanentid%3D4068675%7Cmail%3Dx0219966%40ti.com%7Cuid%3Dx0219966%7Ctype%3Dx%7Crole%3DDistributor%20Marketing%7Cgivenname%3DFrank%7Cgivennamelocallanguage%3D%7Csn%3DQiu%7Csnlocallanguage%3D%7Ccn%3DFrank%20Qiu%7Csecuritylevel%3D1%7Cadminrights%3D%7Coriginalorganizationname%3DTexas%20Instruments%7Crelationship%3DTI%20Internal%7Co%3DTexas%20Instruments%7Colocallanguage%3D%7Cwwacctnum%3D%7Cmodifytimestamp%3D20150416011437Z%7Cauthtimestamp%3D20150427063248Z%7Cstreet%3DIBP%20Shanghai%2C%20Level%203%20-%20Building%204%7Cstreet2%3DNo.168%20Linhong%20Road%7Ccity%3DShanghai%7Cst%3D%7Cpostalcode%3D200335%7Cc%3DCN%7Cshippingstreet%3D%7Cshippingstreet2%3D%7Cshippingcity%3D%7Cshippingst%3D%7Cshippingpostalcode%3D%7Cshippingc%3DCN%7Cregion%3DAmericas%7Ctelephonenumber%3D%7Cfacsimiletelephonenumber%3D%7Cemployeetype%3DEngineering%7Ctitle%3D%7Cwebenchuserid%3D4068675%7Cwebenchoptin%3D%7Cnscuid%3D%7Ccreatedate%3D20140613015519Z%7Cemailready%3D%7Cemailvalidationdate%3D; CREDHASH=310b65971ecb0276b3968a18589cdff4bcf1753e; _loginTime=1430116368"

postURL = "http://ptg.itg.ti.com/prog/dsbga_calc.cgi"

headers = {"Request" : "POST /prog/dsbga_calc.cgi HTTP/1.1",
           "Accept" : "text/html, application/xhtml+xml, */*",
           "Referer" : "http://ptg.itg.ti.com/microSMD/html/dsbga_calc.html",
           "Accept-Language" : "zh-CN",
           "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
           "Content-Type" : "application/x-www-form-urlencoded",
           "Accept-Encoding" : "gzip, deflate",
           "Host" : "ptg.itg.ti.com",
           "Content-Length" : 131,
           "Connection" : "Keep-Alive",
           "Cache-Control" : "no-cache",
           "Cookie" : cookies
     }

postData = {"desg" : "yfu",
            "bump_count" : 15,
            "bump_pitch" : 0,
            "bump_pitchD" : 0,
            "bump_dia" : 0,
            "sideEbumps" : 0,
            "sideDbumps" : 0,
            "sideDsize" : 2.32,
            "sideEsize" : 1.013
            }


encodedData = urllib.urlencode(postData) + "&Submit=Submit"

##print encodedData

request = urllib2.Request(postURL, encodedData, headers)

response = urllib2.urlopen(request)

f= response.read()
filt = re.compile(r'<H1>Assigned TI Outline: (.+)</H1>')
result = filt.search(f).group(1)
print f
print result
