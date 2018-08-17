from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crFullName = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]
outputPath = config.configDict["Output Folder"]
includeVaultComponent = int(config.configDict["Include Vault Components"])
assignHRD = int(config.configDict["Assgin HRID"])
cmpNamingScheme = config.configDict["Component Naming Scheme"]
initialHRIDIndex = config.configDict["Initial HRID Index"]

#=========================================================================================================
print crFullName
print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)

if (crType == "Altium"):
    componentSet = parseAluCR(crFullName)
else:
    componentSet = parseTIcr(crFullName)

cmpEleTree = initCMPtree("Template.xml", client, componentSet.componentList)

if not includeVaultComponent:
    print "checking components in vault"
    cmpVaultItemList = getVaultItemRevisionInfo(client, componentSet.componentList, "CMPLIB")
   
    for cmpVaultItem in cmpVaultItemList:
        cmpFound = 0
        for cmp in componentSet.componentList:
            if cmp.parmeters.has_key("Comment"):
                if cmp.parmeters["Comment"].upper() == cmpVaultItem.Comment.upper():
                    cmpFound = cmp
                    break
        if cmpFound:
            componentSet.componentList.remove(cmpFound)

    # it seems the function of this paragrahp is duplicated with the above one
    #for cmp in componentSet.componentList:
    #    if cmp.parmeters.has_key("Comment"):
    #        for cmpVaultItem in cmpVaultItemList:
    #            if cmp.parmeters["Comment"] == cmpVaultItem.Comment:
    #                componentSet.componentList.remove(cmp)

if assignHRD:
    print "assinging HRID..."
    newCmpHRIDList = retriveItemHRID(cmpNamingScheme, str(initialHRIDIndex), client, len(componentSet.componentList), "CMP")

#query the data of models in DB, get item revision guid. 
if (componentSet.symbolList and componentSet.footprintList):
    print "getting item info from vault"
    symbolVaultItemList = getVaultItemRevisionInfoLatestRev(getVaultItemRevisionInfo(client, componentSet.symbolList, "SCHLIB"))
    footprintVaultItemList = getVaultItemRevisionInfoLatestRev(getVaultItemRevisionInfo(client, componentSet.footprintList, "PCBLIB"))
    
    #start to insert linked models and required parameters
    for vaultItem in symbolVaultItemList:
        linkModelEle = createModelLinkEle(vaultItem, "SCHLIB")
        insertEle(cmpEleTree, linkModelEle, "ModelLinks")

    for vaultItem in footprintVaultItemList:
        linkModelEle = createModelLinkEle(vaultItem, "PCBLIB")
        insertEle(cmpEleTree, linkModelEle, "ModelLinks")

    for reqParam in componentSet.parmeters:
        reqParamEle = createRequiredParamEle(reqParam)
        insertEle(cmpEleTree, reqParamEle, "RequiredParameters")

    for tarFolder in componentSet.tarFolderPath:
        vaultFolderGUID = getSpecificFolderGUID(tarFolder, allFolders)
        if not vaultFolderGUID:
            print "new folder found: " + tarFolder
            print "creating folder..."
            createVaultFolder(tarFolder, allFolders, client)
            allFolders = getVaultFolders(client)

    #create and insert component definition
    print "start to build cmplib"
    pb = progressbarClass(len(componentSet.componentList), "*")
    componentCount = 0
    for component in componentSet.componentList:
        if assignHRD:
            componentHRID = newCmpHRIDList[componentCount]
        else:
            componentHRID = "UNAMED-" + str(componentCount)

        componentEle = createComponentEle(componentHRID,component.symbolList, component.footprintList, component.parmeters)
        #if target vault folder is not defined, insert the component ele in default group
        if not component.tarFolderPath:
            insertEle(cmpEleTree, componentEle, "./TopGroup/Groups/TGroup/ComponentDefinitions")
        else:
            for topGroup in cmpEleTree.findall("./TopGroup"):
                tGroup = insertGroupEle(component.tarFolderPath, topGroup, allFolders)
                insertEle(tGroup, componentEle, "ComponentDefinitions")
   
        pb.progress(componentCount + 1) 
        componentCount += 1

    rebuildCMPIndex(cmpEleTree)

    print ''
    print 'writting to file'

    writeEle2File(cmpEleTree,  OP.join(outputPath, OP.basename(crFullName).replace("." + crFullName.rpartition(".")[2], ".CmpLib")))

else:
    print "symbol or footprints not found in CR"

print "done"
raw_input()