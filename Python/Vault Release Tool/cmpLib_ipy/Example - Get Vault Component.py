import urllib2
import xml.etree.ElementTree as ET
import re

#get vault component revisions data by component name without SDK dependence
vaultAddress = "http://shavault01.altium.biz:9780"
userName = "admin"
passowrd = "admin"
componentName = "INA3221AIRGVR"

def SOAP_RequestPost(requestHeader, requestBody, url):
    requestBodyXML = ET.fromstring(requestBody)

    request = urllib2.Request(url, ET.tostring(requestBodyXML), requestHeader)
    response = urllib2.urlopen(request).read()

    return response

def vaultLogin(vaultAddress, userName, passowrd):
    requestData = '''
                <SOAP-ENV:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                    <SOAP-ENV:Header>
                        <APIVersion xmlns="http://tempuri.org/">2.0</APIVersion>
                    </SOAP-ENV:Header>
                    <SOAP-ENV:Body>
                        <Login xmlns="http://tempuri.org/">
                            <Username>%s</Username>
                            <Password>%s</Password>
                            <SecureLogin>false</SecureLogin>
                            <LoginOptions>None</LoginOptions>
                        </Login>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>
                ''' %(userName, passowrd)
    
    loginURL = vaultAddress + "/ids/?cls=soap"
    headers = {"SOAPAction" : "Login",
               "Content-Type" : 'text/xml; charset="utf-8"',
               "User-Agent" : "Altium Designer" 
        }

    resopnse = SOAP_RequestPost(headers, requestData, loginURL)
    
    sessionId = re.search(r"<SessionId>(.+)</SessionId>", resopnse).group(1)
    return sessionId

def GetALU_ConentTypes(serviceURL, sessionId, contentTypeName):
    requestData = '''
                <SOAP-ENV:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                    <SOAP-ENV:Body>
                        <GetALU_ContentTypes xmlns="http://tempuri.org/">
                            <SessionHandle>%s</SessionHandle>
                            <Options>
                                <item>IncludeAllChildObjects=true</item>
                            </Options>
                            <Filter>HRID in ('%s')</Filter>
                            <InputCursor />
                        </GetALU_ContentTypes>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>
                  '''  %(sessionId, contentTypeName)

    headers = {"SOAPAction" : "GetALU_ContentTypes",
               "Content-Type": 'text/xml; charset="utf-8"',
               "User-Agent": "Altium Designer",
               "Pragma": "no-cache"
        }

    response = SOAP_RequestPost(headers, requestData, serviceURL)

    contentTypeGUID = re.search(r"<GUID>(.+)</GUID>", response).group(1)
    return contentTypeGUID


def GetALU_ItemRevisions(serviceURL, sessionId, comment, contentTypeGUID):
    requestData = '''
                <SOAP-ENV:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                    <SOAP-ENV:Body>
                        <GetALU_ItemRevisions xmlns="http://tempuri.org/">
                            <SessionHandle>%s</SessionHandle>
                            <Options>
                                <item>IncludeItemRevisionParameters=true</item>
                                <item>ExcludeACLEntries=true</item>
                            </Options>
                            <Filter>COMMENT IN ('%s') AND CONTENTTYPEGUID = '%s'</Filter>
                            <InputCursor />
                        </GetALU_ItemRevisions>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>
                    '''  %(sessionId, comment, contentTypeGUID)

    headers = {"SOAPAction" : "GetALU_ContentTypes",
                "Content-Type": 'text/xml; charset="utf-8"',
                "User-Agent": "Altium Designer",
                "Pragma": "no-cache"
        }

    response = SOAP_RequestPost(headers, requestData, serviceURL)
    return response

#loign vault, return session id
sessionHandle = vaultLogin(vaultAddress, userName, passowrd)

serviceURL = vaultAddress + "/vault/?cls=soap" #the client that accepts requries
cmpTypeGUID = GetALU_ConentTypes(serviceURL, sessionHandle, "altium-component") 

#return the component revision data that can be parsed as XML
componentRevisionData = GetALU_ItemRevisions(serviceURL, sessionHandle, componentName, cmpTypeGUID)
print componentRevisionData



