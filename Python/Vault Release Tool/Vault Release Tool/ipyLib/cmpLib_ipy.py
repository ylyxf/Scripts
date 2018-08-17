__author__ = 'frank.qiu'
import clr
clr.AddReferenceToFileAndPath("D:\\Vault SDK\\bin\\DxpServerSDK.dll")
clr.AddReference("system")
import Altium.Sdk.DxpAppServer as VaultSDK
import system

vaultAddress = "http://sample-vault:9780"
loginURL = vaultAddress + "/ids/?cls=soap"
serviceURL = vaultAddress + "/vault/?cls=soap"

idsClient = VaultSDK.IDSClient
loginResult = idsClient.Login("admin", "admin",idsClient, 0)
