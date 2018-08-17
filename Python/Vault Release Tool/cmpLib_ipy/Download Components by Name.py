import sys

def addModelChoiceforComponent(modelRevisionList, modelKind, componentRefId, componentLibraryData):
        for i in xrange(len(modelRevisionList)):
            newModel = modelRevisionList[i]
            rowsModel = componentLibraryData.dataTables["ModelLinks"].lookupRow("RevisionGUID", newModel.RevisionGUID)
            modelId = 0
            for rowModel in rowsModel:
                if rowModel["ModelKind"] == modelKind:
                    modelId = rowModel["refID"]

            if i > 0:
                rowRequiredModel = componentLibraryData.dataTables["RequiredModels"].lookupRow("HRID", modelKind + " " + str(i))
                if not rowRequiredModel:
                    requiredModelId = componentLibraryData.assingRefID()
                    componentLibraryData.dataTables["RequiredModels"].addrequiredModel(modelKind + " " + str(i), modelKind,
                                                                            requiredModelId)
                    componentLibraryData.updateUsedRefID(requiredModelId)
                else:
                    requiredModelId = rowRequiredModel[0]["refID"]

            else:
                rowRequiredModel = componentLibraryData.dataTables["RequiredModels"].lookupRow("HRID", modelKind)
                if not rowRequiredModel:
                    requiredModelId = componentLibraryData.assingRefID()
                    componentLibraryData.dataTables["RequiredModels"].addrequiredModel(modelKind, modelKind,
                                                                            requiredModelId)
                    componentLibraryData.updateUsedRefID(requiredModelId)
                else:
                    requiredModelId = rowRequiredModel[0]["refID"]

            componentLibraryData.dataTables["ModelChoices"].addModelChoice(requiredModelId, modelId,componentRefId)

def addParameter(parameterName, parameterValue, componentRefId, componentLibraryData):
    rowsParam = componentLibraryData.dataTables["RequiredParameters"].lookupRow("HRID", parameterName)
    if rowsParam:
        paramId = rowsParam[0]["refID"]
    else:
        paramId = componentLibraryData.assingRefID()
        componentLibraryData.dataTables["RequiredParameters"].addRequiredParameter(parameterName, paramId)
        componentLibraryData.updateUsedRefID(paramId)

    componentLibraryData.dataTables["ParameterLinks"].addParameterLink(paramId, componentRefId, 
                                                                       parameterValue)


import cmpLib_advanced_ipy as cla
import cmpLib_ipy as cl

config = cl.configInfo()
config.readConfigFile("Config.ini")
vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]

crPath = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]

print "connecting to vault"
client = cl.initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID 


if (crType == "Altium"):
    componentSet = cl.parseAluCR(crPath)
else:
    componentSet = cl.parseTIcr(crPath)


componentData = cla.componentLibrary()

#init group table, add default top group
topGroupId = componentData.assingRefID()
componentData.dataTables["Group"].addGroup("Top Group#",topGroupId, "", "", "")
componentData.updateUsedRefID(topGroupId)
nextGroupId = componentData.assingRefID()
componentData.dataTables["Group"].addGroup("New Group#",nextGroupId, "", "test\\a", topGroupId)
componentData.updateUsedRefID(nextGroupId)

#inti required param table, add comment, description
commentId = componentData.assingRefID()
componentData.dataTables["RequiredParameters"].addRequiredParameter("Comment", commentId)
componentData.updateUsedRefID(commentId)
descId = componentData.assingRefID()
componentData.dataTables["RequiredParameters"].addRequiredParameter("Description", descId)
componentData.updateUsedRefID(descId)


lifeCycle = "C49BAAE1-4B93-4C84-9FD7-CC93C2E8574D"
namingGUID = "E9197BDA-E9EF-4360-8F74-E72904E1C0EE"
componentData.dataTables["BasicInfo"].addBasicInfo(client.VaultInfo.GUID, client.VaultInfo.HRID,
                                                    lifeCycleGUID = lifeCycle,
                                                    revisionNamingGUID = namingGUID)

cmpRevisionList = cl.getVaultItemRevisionInfoLatestRev(cl.getVaultItemRevisionInfo(client, componentSet.componentList, "CMPLIB"))

itemCount = 1
for cmpRevision in cmpRevisionList:
    progressStr = "%s / %s" %(str(itemCount), str(len(cmpRevisionList)))
    sys.stdout.writelines(progressStr + "\r")
    sys.stdout.flush()
    try:
        modelRevisions = cl.getVaultModelsLinkTo(cmpRevision.RevisionGUID, client)
    except Exception, e:
        print e.message
        print "connecting again"
        client = cl.initVaultConnection(vaultAddress, userName, pwd)
        modelRevisions = cl.getVaultModelsLinkTo(cmpRevision.RevisionGUID, client)

    symoblRevisions = []
    footprintRevisions = []
    for modelRev in modelRevisions:
        if modelRev.ContentType == "SCHLIB":
            symoblRevisions.append(modelRev)
        elif modelRev.ContentType == "PCBLIB":
            footprintRevisions.append(modelRev)

        #insert revisions info in library required data tables
        rowsModel = componentData.dataTables["ModelLinks"].lookupRow("RevisionGUID", modelRev.RevisionGUID)
        if rowsModel:
            modelId = rowsModel[0]["refID"]
        else:
            modelId = componentData.assingRefID()
            componentData.dataTables["ModelLinks"].addModelLink(modelRev.HRID, modelId, client.VaultInfo.GUID, modelRev.ItemGUID,
                                                                modelRev.ContentType, modelRev.RevisionGUID, modelRev.RevisionID)
            componentData.updateUsedRefID(modelId)

    #insert component definitions data
    parentGroupId = nextGroupId
    cmpId = componentData.assingRefID()
    componentData.dataTables["ComponentDefinitions"].addComponentDefinition(cmpRevision.HRID, cmpRevision.Comment,
                                                                            parentGroupId, cmpId,
                                                                            itemHRID = cmpRevision.HRID.rpartition("-")[0],
                                                                            revisionGUID = cmpRevision.RevisionGUID,
                                                                            guid = cmpRevision.RevisionGUID)
  
                                                                                
    componentData.updateUsedRefID(cmpId)

    #insert param data
    addParameter("Comment", cmpRevision.Comment, cmpId, componentData)
    addParameter("Description", cmpRevision.Description, cmpId, componentData)
    for paramName in cmpRevision.RevisionsParameters:
        addParameter(paramName, cmpRevision.RevisionsParameters[paramName], cmpId, componentData)

    #insert models for each component
    addModelChoiceforComponent(symoblRevisions, "SCHLIB", cmpId, componentData)
    addModelChoiceforComponent(footprintRevisions, "PCBLIB", cmpId, componentData)

    itemCount += 1


eleData = cla.buildCmplib(componentData.dataTables)
cla.writeEle2File(eleData, crPath.replace(".xls", ".CmpLib"))
print "done"