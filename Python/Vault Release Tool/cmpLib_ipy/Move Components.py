from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crPath = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]

#=============================================================================================================
print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID 

print "getting all folders in vault"
allFolders = getVaultFolders(client)

if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)

#checking if all folders existing before checking the components in vault
for tarFolder in componentSet.tarFolderPath:
    vaultFolderGUID = getSpecificFolderGUID(tarFolder, allFolders)
    if not vaultFolderGUID:
        print "new folder found: " + tarFolder
        print "creating folder..."
        createVaultFolder(tarFolder, allFolders, client)
        allFolders = getVaultFolders(client)

#for path in pathList:
#    folderGUID = getSpecificFolderGUID(path, allFolders)
#    if not folderGUID:
#        print "new folder found: " + path
#        print "creating folder..."
#        createVaultFolder(path, allFolders, client)
#        allFolders = getVaultFolders(client)

print "checking components"
cmpRevisonList = []
if componentSet.componentList:
    cmpRevisonList = getVaultItemRevisionInfo(client, componentSet.componentList, "CMPLIB") 

folderGUIDDict = {} #key is folder path, value is folder GUID
tarFolderDict = {} #key is component revision GUID, value is folder GUID
for component in componentSet.componentList:
    for cmpRevision in cmpRevisonList:
        if cmpRevision.Comment == component.parmeters["Comment"]:
            if folderGUIDDict.has_key(component.tarFolderPath): 
                tarFolderDict[cmpRevision.ItemGUID] = folderGUIDDict[component.tarFolderPath]
            else:
                folderGUID = getSpecificFolderGUID(component.tarFolderPath, allFolders)
                if cmpRevision.FolderGUID != folderGUID:
                    tarFolderDict[cmpRevision.ItemGUID] = folderGUID
                folderGUIDDict[component.tarFolderPath] = folderGUID

print "start to move components"
moveItems(tarFolderDict, client)
print "done"
    
