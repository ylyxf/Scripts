from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crFullName = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]
outputPath = config.configDict["Output Folder"]

print crFullName
print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

if (crType == "Altium"):
    componentSet = parseAluCR(crFullName)
else:
    componentSet = parseTIcr(crFullName)

modelInfoList = getVaultItemInfo(client, componentSet.footprintList, "PCBLIB")

f = open(crFullName.replace("xls", "txt"), "wb")
for mod in modelInfoList:
    print mod.Comment + "^" + mod.RevLastModifiedTime
    try:
        f.write( mod.Comment + "^" + mod.RevLastModifiedTime)
        f.write("\r\n")
    except Exception, e:
        print e.Message
f.close()