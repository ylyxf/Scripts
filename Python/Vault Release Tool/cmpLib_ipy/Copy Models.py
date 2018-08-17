from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crPath = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]
tarFolderPath = config.configDict["Copy  Models to"]
symSrcFolderPath = config.configDict["Symbol Source Folder"]
fpSrcFolderPath = config.configDict["Footprint Source Folder"]
#symVaultFolder = config.configDict["Check Symbol in Vault Folder"]
#fpVaultFolder = config.configDict["Check Footprint in Vault Folder"]
includeVaultModels = int(config.configDict["Copy Vault Models"])

#========================================================================================================================
def removeVaultItemInDict(modelDict, modelType, vaultClient, allVaultFolders = "", targetVaultFolder = ""):
    modelList = []
    for name in modelDict:
        newModel = model(name, "","")
        modelList.append(newModel)

    vaultModelList = getVaultItemInfo(vaultClient, modelList, modelType)

    if allVaultFolders and targetVaultFolder:
        folderGUID = getSpecificFolderGUID(targetVaultFolder, allVaultFolders)
        for vaultModel in vaultModelList:
            if vaultModel.FolderGUID == folderGUID:
                if modelDict.has_key(vaultModel.Comment.upper()):
                    del modelDict[vaultModel.Comment.upper()]

    else:
        for vaultModel in vaultModelList:
            if modelDict.has_key(vaultModel.Comment.upper()):
                del modelDict[vaultModel.Comment.upper()]

if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)

print "connecting vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

#allFolders = getVaultFolders(client)

footprintDict = {}
for footprint in componentSet.footprintList:
    footprintDict[footprint.modelName] = footprint.libName
symbolDict = {}
for symbol in componentSet.symbolList:
    symbolDict[symbol.modelName] = symbol.libName

if not includeVaultModels:
    removeVaultItemInDict(symbolDict, "SCHLIB", client)
    removeVaultItemInDict(footprintDict, "PCBLIB", client)

#start to copy files
for model in symbolDict:
    isCopied = copyFile(symbolDict[model], tarFolderPath, symSrcFolderPath, 0)
    if isCopied:
        print model + " copied"
    
for model in footprintDict:
    isCopied = copyFile(footprintDict[model], tarFolderPath, fpSrcFolderPath, 0)
    if isCopied:
        print model + " copied"

print "done"