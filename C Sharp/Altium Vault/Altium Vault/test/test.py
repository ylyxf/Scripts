import clr
clr.AddReferenceToFileAndPath("D:\\Vault SDK\\bin\\DxpServerSDK.dll")
import Altium.Sdk.DxpAppServer as VaultSDK


def initVaultConnection(vaultAddress, username, passowrd):
    if (vaultAddress == 'http://vault.live.altium.com'):
        loginURL = 'http://ids.live.altium.com/?cls=soap'
        serviceURL = 'http://vault.live.altium.com/?cls=soap'
    else:
        loginURL = vaultAddress + "/ids/?cls=soap"
        serviceURL = vaultAddress + "/vault/?cls=soap"

    idsClient = VaultSDK.IDSClient(loginURL)
    loginResult = idsClient.Login(username, passowrd, False)
    vaultClient = VaultSDK.VaultClient(serviceURL)
    vaultClient.Login(loginResult.SessionId)

    return vaultClient

def getVaultInfo(vaultClient):
    client = vaultClient
    vaultInfo = {}
    vaultInfo["vaultGUID"] = client.VaultInfo.GUID
    vaultInfo['vaultName'] = client.VaultInfo.HRID

    return vaultInfo

def printSth():
    print "xxxxx"

client = initVaultConnection(vaultAdress, userName, passowrd)
print getVaultInfo(client)