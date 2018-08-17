import urllib2
import re
import string
import urllib
import json

def test1():
     headers = {
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
               }
##   result = urllib2.urlopen("http://ciiva.com/partsearch?q=0.1uf%20ceramic%20capacitor", headers=headers)
     request = urllib2.Request("http://ciiva.com/partsearch?q=0.1uf%20ceramic%20capacitor", headers = headers)
     result = urllib2.urlopen(request)
     fi = result.read()
     print fil

def test2():
     url = "https://api.ciiva.com/api/auth/2dc8cd88-4680-4d0d-82df-57bc1271e8c0"
     postData = {"Username" : "qcc2004@hotmail.com",
                 "Password" : "123456"}
     
     encodedData = urllib.urlencode(postData)
     request = urllib2.Request(url, encodedData)
     res = urllib2.urlopen(request)
     f = response.read()
     print f

def test3():
     url = "https://api.ciiva.com/api/auth/apikey"
     postData = {"Username" : "2dc8cd8846804d0d82df57bc1271e8c0",
                 "Password" : "123456"}

     jdata = json.dumps(postData)

     req = urllib2.Request(url, jdata)
     res = urllib2.urlopen(req)
     f = res. read()
     print f


def test4():
     url = "https://api.ciiva.com/api/BDAA3836-DB9B-4CFE-A395-B7CBEA7B4865"
     postData = {"PartNumber" : "MCP2515",
                 "Limit" : "3"}

     jdata = json.dumps(postData)

     req = urllib2.Request(url, jdata)
     res = urllib2.urlopen(req)
     f = res. read()
     print f


test3()
