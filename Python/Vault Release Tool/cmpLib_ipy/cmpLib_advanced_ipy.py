#in this library, cmplib and cr will be present as tables in memory. The data will only be converted to
#xml elements after all work done

import csv
import os
import os.path as OP
import shutil
import xml.etree.ElementTree as ET

class row:
    def __init__(self):
        self.id = 0
        self.data = {}

class table:
    usedRefID = []
    def __init__(self):
        self.tableData = []
        self.rowCount = 0

    def insertRow(self, rowDict):
        rowData = row()
        rowData.id = self.rowCount
        rowData.data = rowDict
        self.tableData.append(rowData)
        self.rowCount += 1
        if rowDict.has_key("refID"):
            if rowDict["refID"] not in self.usedRefID:
                self.usedRefID.append(rowDict["refID"])

    def removeRow(self, rowID):
        for row in self.tableData:
            if row.id == rowID:
                self.tableData.remove(row)
                break

        self.rowCount = 1
        for row in self.tableData:
            row.id = self.rowCount
            self.rowCount += 1

        self.rowCount -= 1

    def updateRow(self, rowID, rowData):
        for row in self.tableData:
            if row.id == rowID:
                row.data = rowData

    def exportColumn(self, header):
        col = []
        for row in self.tableData:
            if row.data.has_key(header):
                col.append(row.data[header])

        return col

    def exportRow(self, rowID):
        rowData = {}
        for row in self.tableData:
            if row.id == rowID:
                rowData = row.data

        return rowData

    def lookupRow(self, header, value):
        matchRowIdList = []
        for row in self.tableData:
            if row.data.has_key(header):
                if row.data[header] == value:
                    matchRowIdList.append(row.id)

        matchRows = []
        for id in matchRowIdList:
            matchRows.append(self.exportRow(id))

        return matchRows


    def lookupRowID(self, header, value):
        matchRowIdList = []
        for row in self.tableData:
            if row.data.has_key(header):
                if row.data[header] == value:
                    matchRowIdList.append(row.id)

        return matchRowIdList


    def printTable(self):
        for row in self.tableData:
            print row.data

    def removeBadChars(self):
        for row in self.tableData:
            for field in row.data:
                try:
                    row.data[field].decode("utf_8")
                except Exception, ex:
                    row.data[field] = "Error!"

    def generateRefID(self):
        refID = 1
        while str(refID) in self.usedRefID:
            refID += 1

        return refID

    def clearContent(self):
        for row in self.tableData:
            if row.data.has_key("refID"):
                if str(row.data["refID"]) in self.usedRefID:
                    self.usedRefID.remove(row.data["refID"])
        self.__init__()

class tableModelChoices(table):
    #def __init__(self, requiredModelRefId, modelLinkRefId, componentId):
    #    self.addModelChoice(requiredModelRefId, modelLinkRefId, componentId)

    def addModelChoice(self, requiredModelRefId, modelLinkRefId, componentRefId, componentName = ""):

        self.insertRow({"RequiredModel":requiredModelRefId, "ModelLink":modelLinkRefId,
                        "Component":componentRefId, "ComponentName":componentName})

class tableRequiredModels(table):
    def addrequiredModel(self, hrid, modelKind, refId, 
                         isRquired = "false", fromTemplate = "false", isReadOnly = "false", visible = "true"):

        self.insertRow({"HRID":hrid, "Visible":visible, "ModelKind":modelKind, "IsRequired":isRquired,
                        "FromTemplate":fromTemplate, "IsReadOnly":isReadOnly, "refID":refId})

class tableGroups(table):
    def addGroup(self, hrid, refId, guid, path, parentGroupRefId, itemNamingScheme = ""):

        self.insertRow({"HRID":hrid, "refID":refId, "GUID":guid, "Path":path, "ParentGroup":parentGroupRefId,
                        "ItemNamingScheme":itemNamingScheme})

class tableComponentDefinitions(table):
    def addComponentDefinition(self, hrid, componentName, parentGroupRefId, refID, componentType = "", itemHRID = "",
                               revisionGUID = "", itemNamingScheme = "", guid = ""):

        self.insertRow({"HRID":hrid, "Comment":componentName, "ParentGroup":parentGroupRefId, "ComponentTypes":componentType,
                        "refID":refID, "ItemHRID":itemHRID, "RevisionGUID":revisionGUID, "ItemNamingScheme":itemNamingScheme,
                        "GUID":guid})

class tableRequiredParameters(table):
    def addRequiredParameter(self, hrid, refId, visible = "true", isRequired = "false", dataType = "Text",
                             paramType = "4884412E-AAD1-4E69-922A-23C1C75250B1", defaultValue = "", isReadOnly = "False"):

        
        self.insertRow({"HRID":hrid, "refID":refId, "Visible":visible, "IsRequired":isRequired, "DataType":dataType,
                        "ParamType":paramType, "DefaultValue":defaultValue, "IsReadOnly":isReadOnly})

class tableParameterLinks(table):
    def addParameterLink(self, requiredParamRefId, componentRefId, paramValue, realValue = "", paramName = "", componentName = ""):

        self.insertRow({"RequiredParameter":requiredParamRefId, "Component":componentRefId, "Value":paramValue, "RealValue":realValue,
                        "Name":paramName, "ComponentName":componentName})

class tableModelLinks(table):
    def addModelLink(self, hrid, refId, vaultGUID, itemGUID, modelKind, revisionGUID, revisionId, 
                     fromTemplate = "false", modelName = ""):

        self.insertRow({"HRID":hrid, "refID":refId, "VaultGUID":vaultGUID, "ItemGUID":itemGUID, "ModelKind":modelKind,
                        "RevisionGUID":revisionGUID, "RevisionId":revisionId, "FromTemplate":fromTemplate, "ModelName":modelName})

class tableBasicInfo(table):
    def addBasicInfo(self, vaultGUID, vaultName, lifeCycleGUID = "", revisionNamingGUID = "", templateGUID = "",
                     templateRevisionGUID = ""):

        self.insertRow({"VaultGUID":vaultGUID, "VaultName":vaultName, "LifeCycleDefinitionGUID":lifeCycleGUID, 
                        "RevisionNamingSchemeGUID":revisionNamingGUID, "TemplateVaultGUID":templateGUID, "TemplateRevisionGUID":templateRevisionGUID})


class componentLibrary():
    usedRefID = []

    def __init__(self):
        self.dataTables = {}
        self.dataTables["ModelChoices"] = tableModelChoices()
        self.dataTables["RequiredModels"] = tableRequiredModels()
        self.dataTables["Group"] = tableGroups()
        self.dataTables["ComponentDefinitions"] = tableComponentDefinitions()
        self.dataTables["RequiredParameters"] = tableRequiredParameters()
        self.dataTables["ParameterLinks"] = tableParameterLinks()
        self.dataTables["ModelLinks"] = tableModelLinks()
        self.dataTables["BasicInfo"] = tableBasicInfo()

    def assingRefID(self):
        refID = 1
        while refID in self.usedRefID:
            refID += 1

        return refID

    def updateUsedRefID(self, refID):
        if refID not in self.usedRefID:
            self.usedRefID.append(refID)      

#convert the data which is parsed from component record to cmplib style
#data is parsed by cmplib_ipy.parseTIRecord or parseAluRecord, it's a instance of componentSet
#by this function, no vault data will be included
def parseCrData(crComponentSet):
    #pass the model list of class Component, the required model table and model choice table will be updated
    def insertModelsforComponent(modelList, modelKind, componentRefId, componentLibraryData):
        for i in xrange(len(modelList)):
            newModel = modelList[i]
            rowsModel = componentLibraryData.dataTables["ModelLinks"].lookupRow("ModelName", newModel.modelName)
            modelId = 0
            for rowModel in rowsModel:
                if rowModel["ModelKind"] == modelKind:
                    modelId = rowModel["refID"]

            if i > 0:
                rowRequiredModel = componentLibraryData.dataTables["RequiredModels"].lookupRow("HRID", modelKind + " " + str(i))
                if not rowRequiredModel:
                    requiredModelId = cmpData.assingRefID()
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

    cmpData = componentLibrary()
    #establish required data tables
    for symbol in crComponentSet.symbolList:
        symbolId = cmpData.assingRefID()
        cmpData.dataTables["ModelLinks"].addModelLink("", symbolId, "", "", "SCHLIB", "", "",
                                                      modelName = symbol.modelName)
        cmpData.updateUsedRefID(symbolId)
    
    for footprint in crComponentSet.footprintList:
        footprintId = cmpData.assingRefID()
        cmpData.dataTables["ModelLinks"].addModelLink("", footprintId, "", "", "PCBLIB", "", "",
                                                      modelName = footprint.modelName)
        cmpData.updateUsedRefID(footprintId)

    for paramName in crComponentSet.parmeters:
        paramId = cmpData.assingRefID()
        cmpData.dataTables["RequiredParameters"].addRequiredParameter(paramName,paramId)
        cmpData.updateUsedRefID(paramId)
    
    #init group table, add default top group
    topGroupId = cmpData.assingRefID()
    cmpData.dataTables["Group"].addGroup("Top Group#",topGroupId, "", "", "")
    cmpData.updateUsedRefID(topGroupId)

    #add folders into group table
    parentGroupId = topGroupId
    for vaultPath in crComponentSet.tarFolderPath:
        for folder in vaultPath.split("\\"):
            groupPath = vaultPath.partition(folder)[0] + folder
            groupId = cmpData.assingRefID()
            cmpData.dataTables["Group"].addGroup(folder, groupId, "", groupPath, parentGroupId)
            cmpData.updateUsedRefID(groupId)
            parentGroupId = groupId
    
    #insert component info for each part
    for aComponent in crComponentSet.componentList:
        parentGroupId = cmpData.dataTables["Group"].lookupRow("Path", aComponent.tarFolderPath)[0]["refID"]
        if aComponent.parmeters.has_key("Comment"):
            cmpName = aComponent.parmeters["Comment"]
        else:
            cmpName = "#NA"

        cmpId = cmpData.assingRefID()
        cmpData.dataTables["ComponentDefinitions"].addComponentDefinition("", cmpName, parentGroupId, cmpId)
        cmpData.updateUsedRefID(cmpId)

        insertModelsforComponent(aComponent.symbolList, "SCHLIB", cmpId, cmpData)
        insertModelsforComponent(aComponent.footprintList, "PCBLIB", cmpId, cmpData)

        for paramName in aComponent.parmeters:
            requiredParamId = cmpData.dataTables["RequiredParameters"].lookupRow("HRID", paramName)[0]["refID"]
            cmpData.dataTables["ParameterLinks"].addParameterLink(requiredParamId, cmpId, aComponent.parmeters[paramName])
    
    return cmpData


def getTextFromChildEle(parentEle, childEleTag ):
    text = ""
    for ele in parentEle.findall("./" + childEleTag):
        text = ele.text

    return  text

def parseCmpLib(filePath):
    def buildReqDataTable(tagName, dataTable):
        for reqEle in eleCmplib.iter(tagName):
            refID = reqEle.get("id")
            tables.updateUsedRefID(int(refID))
            row = {"refID" : refID}
            for item in reqEle:
                row[item.tag] = item.text

            dataTable.insertRow(row)

    def buildGroupTable():#import component folders
        topSetting = ""
        #get the info of top group(it's not the top level folder!)
        for topGroupEle in eleCmplib.findall("./TopGroup"):
            topSetting = topGroupEle
            refID =topGroupEle.get("id")
            tables.updateUsedRefID(refID)
            guid = getTextFromChildEle(topGroupEle, "GUID")
            itemNaming = getTextFromChildEle(topGroupEle, "ItemNamingScheme")

            tables.dataTables["Group"].insertRow({"HRID":"Top Group#", "refID":refID,
                                                  "GUID":guid, "Path":"",
                                                  "ParentGroup":"", "ItemNamingScheme": itemNaming})

        #traverse the path, get all folders
        for tGroupEle in topSetting.findall(".//TGroup"):
            refID = tGroupEle.get("id")
            tables.updateUsedRefID(refID)
            guid = ""
            guid = getTextFromChildEle(tGroupEle, "GUID")
            hrid = getTextFromChildEle(tGroupEle, "HRID")
            path = getTextFromChildEle(tGroupEle, "Path")
            for parentGroupEle in tGroupEle.findall("./ParentGroup"):
                parentGroup = parentGroupEle.get("href").replace("#", "")

            tables.dataTables["Group"].insertRow({"HRID":hrid, "refID":refID,
                                                  "GUID":guid, "Path":path,
                                                  "ParentGroup":parentGroup, "ItemNamingScheme":""})

    def buildCmpTableSet():
        for cmpEle in eleCmplib.findall(".//TComponentDefinition"):
            cmpID = tables.assingRefID()
            guid = getTextFromChildEle(cmpEle, "GUID")
            hrid = getTextFromChildEle(cmpEle, "HRID")
            cmpType = getTextFromChildEle(cmpEle, "ComponentTypes")
            itemHRID = getTextFromChildEle(cmpEle, "ItemHRID")
            revGUID = getTextFromChildEle(cmpEle, "RevisionGUID")
            namingScheme = getTextFromChildEle(cmpEle, "ItemNamingScheme")
            for parentGroupEle in cmpEle.findall("./ParentGroup"):
                parentGroup = parentGroupEle.get("href").replace("#", "")

            tables.dataTables["ComponentDefinitions"].insertRow({"HRID":hrid, "GUID":guid, "ParentGroup":parentGroup,
                                                                "ComponentTypes":cmpType, "ItemHRID":itemHRID,
                                                                "RevisionGUID":revGUID, "ItemNamingScheme":namingScheme,
                                                                "refID":cmpID})

            for tParamEle in cmpEle.findall(".//TParameter"):
                paramValue = getTextFromChildEle(tParamEle, "Value")
                realValue = getTextFromChildEle(tParamEle, "RealValue")
                for reqParamEle in tParamEle.iter("RequiredParameter"):
                    reqParam = reqParamEle.get("href").replace("#", "")

                tables.dataTables["ParameterLinks"].insertRow({"RequiredParameter":reqParam, "Value":paramValue,
                                                                "RealValue":realValue, "Component":cmpID})

            for modelEle in cmpEle.findall(".//TModelChoice"):
                for reqModelEle in modelEle.iter("RequiredModel"):
                    reqModel = reqModelEle.get("href").replace("#", "")
                for modelLinkEle in modelEle.iter("ModelLink"):
                    modelLink = modelLinkEle.get("href").replace("#", "")

                tables.dataTables["ModelChoices"].insertRow({"RequiredModel":reqModel, "ModelLink":modelLink,
                                                            "Component":cmpID})

            tables.updateUsedRefID(cmpID)

    def addComponentComment():
        commentParamID = tables.dataTables["RequiredParameters"].lookupRow("HRID", "Comment")[0]["refID"]
        commentParamList = tables.dataTables["ParameterLinks"].lookupRow("RequiredParameter", commentParamID)

        for comment in commentParamList:
            componentID = comment["Component"]
            componentRowID = tables.dataTables["ComponentDefinitions"].lookupRowID("refID", componentID)[0]

            componentRowData = tables.dataTables["ComponentDefinitions"].lookupRow("refID", componentID)[0]
            componentRowData["Comment"] = comment["Value"]

            tables.dataTables["ComponentDefinitions"].updateRow(componentRowID, componentRowData)

    tables = componentLibrary()
    parser = ET.XMLParser(encoding="utf-8")
    eleCmplib = ET.parse(filePath, parser=parser)

    #import all required models and parameters tables
    buildReqDataTable("TRequiredParameter", tables.dataTables["RequiredParameters"])
    buildReqDataTable("TRequiredModel", tables.dataTables["RequiredModels"])
    buildReqDataTable("TModelLink", tables.dataTables["ModelLinks"])

    #import components data, model choices, parameter links
    buildGroupTable()
   
    componentTables = buildCmpTableSet()

    #import basic cmplib info
    lifeCycleGUID = getTextFromChildEle(eleCmplib, "LifeCycleDefinitionGUID")
    revNamingGUID = getTextFromChildEle(eleCmplib, "RevisionNamingSchemeGUID")
    vaultGUID = getTextFromChildEle(eleCmplib, "VaultGUID")
    vaultName = getTextFromChildEle(eleCmplib, "VaultName")
    tempVaultGUID = getTextFromChildEle(eleCmplib, "TemplateVaultGUID")
    tempRevGUID = getTextFromChildEle(eleCmplib, "TemplateRevisionGUID")

    tables.dataTables["BasicInfo"].insertRow({"LifeCycleDefinitionGUID":lifeCycleGUID,
                                              "RevisionNamingSchemeGUID":revNamingGUID,
                                              "VaultGUID":vaultGUID,
                                              "VaultName":vaultName,
                                              "TemplateVaultGUID":tempVaultGUID,
                                              "TemplateRevisionGUID":tempRevGUID})

    addComponentComment()

    for aTable in tables.dataTables:
        tables.dataTables[aTable].removeBadChars
    return tables


def buildCmplib(cmpDataTables):
    eleCmplib = ET.Element("TComponentSet")
    eleCmplib.set("id", "0")

    #export basic cmplib info elements
    basicInfos = cmpDataTables["BasicInfo"].tableData[0].data
    for field in basicInfos:
        infoEle = ET.SubElement(eleCmplib, field)
        infoEle.text = basicInfos[field]

    reqDataTableNames = {"RequiredParameters" : "TRequiredParameter",
                        "RequiredModels" : "TRequiredModel",
                        "ModelLinks" : "TModelLink"}

    #export required models, parameters elements
    for reqDataTable in reqDataTableNames:
        if cmpDataTables.has_key(reqDataTable):
            reqDataEle = ET.SubElement(eleCmplib, reqDataTable)
            for tReqData in cmpDataTables[reqDataTable].tableData:
                tReqDataEle = ET.SubElement(reqDataEle, reqDataTableNames[reqDataTable])
                tReqDataEle.set("id", str(tReqData.data["refID"]))
                for header in tReqData.data:
                    if not (header == "refID"):
                        itemEle = ET.SubElement(tReqDataEle, header)
                        itemEle.text = tReqData.data[header]

    #export components data:
    if cmpDataTables.has_key("ComponentDefinitions"):
        cmpTable = cmpDataTables["ComponentDefinitions"].tableData
        cmpDataEleDict = {} #refID is key, value is list of TComponentDefinition elements

        for tCmpDef in cmpTable:
            tCmpDefEle = ET.Element("TComponentDefinition")
            tCmpDefEle.set("StateIndex", "2")
            for header in tCmpDef.data:
                if header == "ParentGroup":
                    parentGroupEle = ET.SubElement(tCmpDefEle, header)
                    parentGroupEle.set("href", "#" + str(tCmpDef.data[header]))
                elif header =="refID":
                    continue
                else:
                    itemEle = ET.SubElement(tCmpDefEle, header)
                    itemEle.text = tCmpDef.data[header]

            #process model and parameter part
            cmpID = tCmpDef.data["refID"]
            paramList = cmpDataTables["ParameterLinks"].lookupRow("Component", cmpID)
            paramEle = ET.SubElement(tCmpDefEle, "Parameters")
            for param in paramList:
                tParamEle = ET.SubElement(paramEle, "TParameter")
                for header in param:
                    if header == "RequiredParameter":
                        reqParamEle = ET.SubElement(tParamEle, header)
                        reqParamEle.set("href", "#" + str(param[header]))
                    elif header == "Component":
                        continue
                    elif header == "RealValue":
                        itemEle = ET.SubElement(tParamEle, header)
                        if param[header]: 
                            itemEle.text = param[header]
                        else:
                            itemEle.text = "NaN"
                    else:
                        itemEle = ET.SubElement(tParamEle, header)
                        itemEle.text = param[header]

            modelList = cmpDataTables["ModelChoices"].lookupRow("Component", cmpID)
            modelChoiceEle = ET.SubElement(tCmpDefEle, "ModelChoices")
            for model in modelList:
                tModelChoiceEle = ET.SubElement(modelChoiceEle, "TModelChoice")
                for header in model:
                    if header == "Component":
                        continue
                    else:
                        itemEle = ET.SubElement(tModelChoiceEle, header)
                        itemEle.set("href", "#" + str(model[header]))

            #add component element into list accroding to its group
            refID = tCmpDef.data["ParentGroup"]
            if cmpDataEleDict.has_key(refID):
                cmpDataEleDict[refID].append(tCmpDefEle)
            else:
                cmpDataEleDict[refID] = [tCmpDefEle]


    #export component groups
    if cmpDataTables.has_key("Group"):
        topGroup = cmpDataTables["Group"].lookupRow("HRID", "Top Group#")[0]
        topGroupEle = ET.SubElement(eleCmplib, "TopGroup")
        topGroupEle.set("StateIndex", "2")
        topGroupEle.set("Collapsed", "false")
        componentSetEle = ET.SubElement(topGroupEle, "ComponentSet")
        componentSetEle.set("href", "#0")

        groupsEle = ET.SubElement(topGroupEle, "Groups")

        for header in topGroup:
            if header == "refID":
                topGroupEle.set("id", str(topGroup[header]))
            else:
                itemEle = ET.SubElement(topGroupEle, header)
                itemEle.text = topGroup[header]

        for refID in cmpDataEleDict:
            group = cmpDataTables["Group"].lookupRow("refID", refID)[0]
            tGroupEle = ET.SubElement(groupsEle, "TGroup")
            parentGroupEle = ET.SubElement(tGroupEle, "ParentGroup")
            parentGroupEle.set("href", "#" + str(topGroup["refID"]))
            componentSetEle = ET.SubElement(tGroupEle, "ComponentSet")
            componentSetEle.set("href", "#0")
            cmpDefsEle = ET.SubElement(tGroupEle, "ComponentDefinitions")

            for header in  group:
                if header == "refID":
                    tGroupEle.set("id", str(group[header]))
                elif header == "ParentGroup":
                    continue
                else:
                    itemEle = ET.SubElement(tGroupEle, header)
                    itemEle.text = group[header]

            cmpDefsEle.extend(cmpDataEleDict[refID])

    return eleCmplib

def writeEle2File(element, filePath):
    eleTree = ET.ElementTree(element)
    f = open(filePath, "wb")
    eleTree.write(f, xml_declaration = True, encoding= "utf-8",method="xml")
    f.close()


