from cmpLib_ipy import *

vaultAddress = "http://shavault01.altium.biz:9780"
userName = "admin"
pwd = "admin"
crPath = r"G:\newcontentteam\Components\TIRequestSource\DatabaseLibraries-0604\Capacitor-Aluminum.csv"
crType = "TI"
outputPath = r"G:\newcontentteam\Components\TIRequestSource\DatabaseLibraries-0604"
includeVaultComponent = 0

#=========================================================================================================
print crPath
print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)

cmpEleTree = initCMPtree("Template.xml", client)
if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)

if not includeVaultComponent:
    print "checking components in vault"
    cmpVaultItemList = getBatchVaultItemInfofromVault(client, componentSet.componentList, "CMP")

    for cmpVaultItem in cmpVaultItemList:
        cmpFound = 0
        for cmp in componentSet.componentList:
            if cmp.parmeters.has_key("Comment"):
                if cmp.parmeters["Comment"] == cmpVaultItem.Comment:
                    cmpFound = cmp
                    break
        if cmpFound:
            componentSet.componentList.remove(cmpFound)

    for cmp in componentSet.componentList:
        if cmp.parmeters.has_key("Comment"):
            for cmpVaultItem in cmpVaultItemList:
                if cmp.parmeters["Comment"] == cmpVaultItem.Comment:
                    componentSet.componentList.remove(cmp)

#query the data of models in DB, get item revision guid.
if (componentSet.symbolList and componentSet.footprintList):
    print "getting item info from vault"
    symbolVaultItemList = getBatchVaultItemInfofromVault(client, componentSet.symbolList, "SCHLIB")
    footprintVaultItemList = getBatchVaultItemInfofromVault(client, componentSet.footprintList, "PCBLIB")

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

    #create and insert component definition
    print "start to build cmplib"
    pb = progressbarClass(len(componentSet.componentList), "*")
    componentCount = 0
    for component in componentSet.componentList:
        componentHRID = "UNAMED-" + str(componentCount)
        componentEle = createComponentEle(componentHRID,component.symbolList, component.footprintList, component.parmeters)
        vaultFolderGUID = getSpecificFolderGUID(component.tarFolderPath, allFolders)
        if not vaultFolderGUID:
            insertEle(cmpEleTree, componentEle, "./TopGroup/Groups/TGroup/ComponentDefinitions")
        else:
            for topGroup in cmpEleTree.findall("./TopGroup"):
                tGroup = insertGroupEle(component.tarFolderPath, topGroup, allFolders)
                insertEle(tGroup, componentEle, "ComponentDefinitions")

        pb.progress(componentCount)
        componentCount += 1

    rebuildCMPIndex(cmpEleTree)

    print ''
    print 'writting to file'
    writeEle2File(cmpEleTree,  OP.join(outputPath, OP.basename(crPath)).replace(".csv", ".CmpLib"))

else:
    print "symbol or footprints not found in CR"