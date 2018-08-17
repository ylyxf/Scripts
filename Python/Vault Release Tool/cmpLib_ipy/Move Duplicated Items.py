import csv
import xlrd
import os
import os.path as OP
import shutil
import xml.etree.ElementTree as ET
import json
import clr
from System import *
#clr.AddReferenceToFileAndPath("DxpServerSDK.dll")
clr.AddReferenceToFileAndPath("D:\\Vault SDK\\bin\\DxpServerSDK.dll")
import Altium.Sdk.DxpAppServer as VaultSDK
import Altium.Sdk.DxpAppServer.IDSServiceProxy

vaultAddress = "https://shacontent-vat.altium.biz:9785"
userName = "admin"
pwd = "admin"

loginURL = vaultAddress + "/ids/?cls=soap"
serviceURL = vaultAddress + "/vault/?cls=soap"
idsClient = VaultSDK.IDSClient(loginURL)

try:
    loginResult = idsClient.Login(userName, pwd, True, Altium.Sdk.DxpAppServer.IDSServiceProxy.LoginOptions.KillExistingSession)
    vaultClient = VaultSDK.VaultClient(serviceURL)
    vaultClient.Login(vaultClient.SessionID)

except Exception, e:
    print e.Message