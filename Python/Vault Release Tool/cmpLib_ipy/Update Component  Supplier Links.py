from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crFullName = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]

print crFullName
print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

if (crType == "Altium"):
    componentSet = parseAluCR(crFullName)
else:
    componentSet = parseTIcr(crFullName)

vaultCmpRevList = getVaultItemRevisionInfoLatestRev(getVaultItemRevisionInfo(client, componentSet.componentList, "CMPLIB"))

guid2MPNDict = {} #key is vault component guid, value is mpn/vendor name pair
for vaultCmpRev in vaultCmpRevList:
    for cmp in componentSet.componentList:
        if cmp.parmeters["Comment"] == vaultCmpRev.Comment:
            if not cmp.parmeters.has_key("Manufacturer"):
                break

            if cmp.parmeters["Manufacturer"]:
                guid2MPNDict[vaultCmpRev.RevisionGUID] = (cmp.parmeters["Comment"], cmp.parmeters["Manufacturer"])

for itemRevGUID in guid2MPNDict:
    result = releasePartChoice(client, itemRevGUID, guid2MPNDict[itemRevGUID][0], guid2MPNDict[itemRevGUID][1])
    
    print guid2MPNDict[itemRevGUID][0] + " " + result

print "done"