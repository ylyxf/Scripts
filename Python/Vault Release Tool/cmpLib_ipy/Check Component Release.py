from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crFolder = config.configDict["Component Records Folder"]
crType = config.configDict["Component Record Type"]
fileExtention = config.configDict["Record File Extension"]
outputPath = config.configDict["Output Folder"]

print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)

recordList = traversalFolder(crFolder, fileExtention)

componentSetCollection = {}
componentNumberinAllRecords = 0
print "checking component records..."

for record in recordList:   
    print OP.basename(record)
    if (crType == "Altium"):
        componentSet = parseAluCR(record)
    else:
        componentSet = parseTIcr(record)

    cmpVaultItemList = getVaultItemRevisionInfo(client, componentSet.componentList, "CMPLIB")
    for cmpVaultItem in cmpVaultItemList:
            cmpFound = 0
            for cmp in componentSet.componentList:
                if cmp.parmeters.has_key("Comment"):
                    if cmp.parmeters["Comment"] == cmpVaultItem.Comment:
                        cmpFound = cmp
                        break
            if cmpFound:
                componentSet.componentList.remove(cmpFound)

    print str(len(componentSet.componentList)) + " not released"
    
    f = open(record.replace(fileExtention, "txt"), "wb")
    for cmp in componentSet.componentList:
        f.write(cmp.parmeters["Comment"])
        f.write("\r\n")
    f.close()