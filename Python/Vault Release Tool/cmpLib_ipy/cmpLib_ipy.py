import csv
from collections import OrderedDict
import xlrd, xlwt
import os, sys
import os.path as OP
import shutil
import xml.etree.ElementTree as ET
import json
import clr
from System import *

class vaultItemRevision:
    def __init__(self, RevisionGUID, Comment, ItemGUID, RevisionID, HRID, FolderGUID, VaultGUID = "",
                 ContentType = "", RevisionDescription = "", RevisionsParameters = {}):
        self.RevisionGUID = RevisionGUID
        self.Comment = Comment
        self.ItemGUID = ItemGUID
        self.RevisionID = RevisionID
        self.HRID = HRID
        self.FolderGUID = FolderGUID
        self.VaultGUID = VaultGUID
        self.ContentType = ContentType
        self.Description = RevisionDescription
        self.RevisionsParameters = RevisionsParameters

class vaultItemInfo:
    def __init__(self, Comment, ItemGUID, HRID, FolderGUID, description):
        self.Comment = Comment
        self.ItemGUID = ItemGUID
        self.HRID = HRID
        self.FolderGUID = FolderGUID
        self.Description = description

class model:
    def __init__(self, modelName, libName, vaultFolder):
        self.modelName = modelName
        self.libName = libName
        self.vaultFolder = vaultFolder

class component:
    def __init__(self, symbolList, footprintList, parmeters, tarFolderPath):
        self.symbolList = symbolList
        self.footprintList = footprintList
        self.parmeters = parmeters  #dict
        self.tarFolderPath = tarFolderPath

class componentSet(component):
    def __init__(self, componentList):
        self.componentList = componentList


class vaultFolder:
    guid = ""
    parentFolderGUID = ""
    folderName = ""
    isRoot = 0
    isLeaf = 0

    def __init__(self, guid, parentFolderGUID, folderName, isRoot, isLeaf):
        self.folderName= folderName
        self.guid = guid
        self.parentFolderGUID = parentFolderGUID
        self.isRoot = isRoot
        self.isLeaf = isLeaf

class configInfo:
    configDict = {}
 
    def readConfigFile(self, filePath):
        for line in open(filePath):
            if not line.startswith("#"):
                if "=" in line:
                    self.configDict[line.partition("=")[0].strip()] = line.partition("=")[2].strip()

#import vault sdk and ciiva sdk
scriptPath = os.getcwd()
sys.path.append("scriptPath")
debugConfig = configInfo()
debugConfig.readConfigFile("Config.ini")
debugMode = int(debugConfig.configDict["Debug"])

if debugMode:
    vautlSDKPath = "D:\\Vault SDK 3.0.0.23\\bin\\DxpServerSDK.dll"
    ciivaAPIPath = "G:\\Scripts\\C Sharp\\Ciiva API Library\\Ciiva API\\bin\\Debug\\CiivaApis.dll"
else:
    vautlSDKPath = scriptPath + "\\Vault SDK\\DxpServerSDK.dll"
    ciivaAPIPath = scriptPath + "\\Ciiva API\\CiivaApis.dll"

clr.AddReferenceToFileAndPath(vautlSDKPath)
clr.AddReferenceToFileAndPath(ciivaAPIPath)
import Altium.Sdk.DxpAppServer as VaultSDK
import Altium.Sdk.DxpAppServer.IDSServiceProxy
import CiivaApis as Ciiva
ciivaAPI = Ciiva.Apis()


contentTypeDict = {VaultSDK.ContentTypeGuid.cSymbol: "SCHLIB",
                   VaultSDK.ContentTypeGuid.cPcbComponent: "PCBLIB",
                   VaultSDK.ContentTypeGuid.cComponent: "CMPLIB"}


def initVaultConnection(vaultAddress, username, passowrd):
    if (vaultAddress == 'http://vault.live.altium.com'):
        loginURL = 'http://ids.live.altium.com/?cls=soap'
        serviceURL = 'http://vault.live.altium.com/?cls=soap'
    else:
        loginURL = vaultAddress + "/ids/?cls=soap"
        serviceURL = vaultAddress + "/vault/?cls=soap"

    idsClient = VaultSDK.IDSClient(loginURL)
    try:
        if debugMode:
            loginResult = idsClient.Login(username, passowrd, False, Altium.Sdk.DxpAppServer.IDSServiceProxy.LoginOptions.KillExistingSession)
        else:
            loginResult = idsClient.Login(username, passowrd, False)
        vaultClient = VaultSDK.VaultClient(serviceURL)
        vaultClient.Login(loginResult.SessionId)
        return vaultClient

    except Exception, e:
        print e.Message
        raw_input()
        return ""
  

def getVaultInfo(vaultClient):
    client = vaultClient
    vaultInfo = {}
    vaultInfo["vaultGUID"] = client.VaultInfo.GUID
    vaultInfo['vaultName'] = client.VaultInfo.HRID

    return vaultInfo

def joinList2String(aList, delimiter):
    resultString = ""
    for item in aList:
        if item:
            resultString = resultString + delimiter + item
            resultString = resultString.lstrip(delimiter)
            
    return resultString


def getVaultFolders(vaultClient):
    folderList = vaultClient.GetAllFolders()

    vaultFolders = []
    for folder in folderList:
        newFolder = vaultFolder(folder.GUID, folder.ParentFolderGUID, folder.HRID, 0, 1)
        if not newFolder.parentFolderGUID: #this check is not reliable. Some folder is with paraent folderGUID, but it do be a root. So be careful!
            newFolder.isRoot = 1

        vaultFolders.append(newFolder)

    return vaultFolders

def getVaultFolderByGUID(folderGUID, allFolders):
    matchFolder = ""
    for folder in allFolders:
        if folder.guid == folderGUID:
            matchFolder = folder
            break

    return matchFolder

def getFullPathbyVaultFolder(vaultFolder, allFolders):
    currentFolder = vaultFolder
    fullPath = currentFolder.folderName

    if currentFolder.isRoot == 1:
        return fullPath
        
    else:
        while not currentFolder.isRoot:
            currentFolder = getVaultFolderByGUID(currentFolder.parentFolderGUID, allFolders)
            if currentFolder == "": #in practise, it seems there are some folders with invalid parent folder GUID
                return fullPath
            else:
                fullPath = currentFolder.folderName +  "\\" + fullPath

        return fullPath  

def getFullPathbyFolderGUID(folderGUID, allFolders):
    matchFolder = getVaultFolderByGUID(folderGUID, allFolders)
    fullPath = getFullPathbyVaultFolder(matchFolder, allFolders)

    return fullPath
  

def setLeafFolder(allVaultFolders):
    for folder in allVaultFolders:
        if folder.parentFolderGUID:
            tarFolder = getVaultFolderByGUID(folder.parentFolderGUID, allVaultFolders)
            if tarFolder:
                tarFolder.isLeaf = 0

    return allVaultFolders

def getSpecificFolderGUID(folderPath, vaultFolders):
    folderGUID = ""
    pathList = []

    if "/" in folderPath:
        folderPath = folderPath.replace("/", "\\")

    if "\\" in folderPath:
        pathList = folderPath.split("\\")
    else:
        pathList.append(folderPath)

    pathList.reverse()

    for folder in vaultFolders:
        if (folder.folderName.upper() == pathList[0].upper()):
            matchPath = getFullPathbyVaultFolder(folder, vaultFolders)
            if matchPath.upper() == folderPath.upper():
                folderGUID = folder.guid

    return folderGUID    


def getVaultItemInfo(vaultClient, componentOrModelList, itemType):
    if itemType == "SCHLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.cSymbol
    elif itemType == "PCBLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.PcbComponent
    elif itemType == "CMPLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.cComponent
    else:
        itemTypeGUID = ""

    itemInfoList = []
    itemListGroup = groupList(componentOrModelList, 500)
    for itemList in itemListGroup:
        queryItemList = [] 
        for item in itemList:
            if itemTypeGUID == VaultSDK.ContentTypeGuid.cComponent:
                if item.parmeters.has_key("Comment"):
                    queryItemList.append("'" + item.parmeters["Comment"] + "'")
            else:
                queryItemList.append("'" + item.modelName + "'")

        queryItemListStr = joinList2String(queryItemList, ",")
        if queryItemListStr:
            queryString = "REVCOMMENT in (" + queryItemListStr + ") AND CONTENTTYPEGUID = '" + itemTypeGUID + "'"
            try:
                vaultItemInfoList = vaultClient.GetItemsInfo(queryString)
            except Exception, e:
                print e.Message
                vaultItemInfoList = ""

            for itemInfo in vaultItemInfoList:
                info = vaultItemInfo(itemInfo.RevComment, itemInfo.GUID, itemInfo.HRID,
                                     itemInfo.FolderGUID, itemInfo.RevDescription)
                itemInfoList.append(info)

    return itemInfoList


def getVaultItemRevisionInfo(vaultClient, componentOrModelList, itemType):
    if itemType == "SCHLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.cSymbol
    elif itemType == "PCBLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.PcbComponent
    elif itemType == "CMPLIB":
        itemTypeGUID = VaultSDK.ContentTypeGuid.cComponent
    else:
        itemTypeGUID = ""

    
    itemRevisionList = []
    itemListGroup = groupList(componentOrModelList, 500)
    for itemList in itemListGroup:
        queryItemList = []  #add quotation mark for every item name to prepare for query string
        for item in itemList:
            if itemTypeGUID == VaultSDK.ContentTypeGuid.cComponent:
                if item.parmeters.has_key("Comment"):
                    queryItemList.append("'" + item.parmeters["Comment"] + "'")
            else:
                queryItemList.append("'" + item.modelName + "'")
                 
        queryItemListStr = joinList2String(queryItemList, ",")
        if queryItemListStr:
            queryString = "COMMENT in (" + queryItemListStr + ") AND CONTENTTYPEGUID = '" + itemTypeGUID + "'"
            try:
                vaultItemRevisionList = vaultClient.GetItemRevisions(queryString)
            except Exception, e:
                print e.Message     
                vaultItemRevisionList = ""

            for revision in vaultItemRevisionList:
                itemRevision = vaultItemRevision(revision.GUID, \
                                                 revision.Comment, \
                                                 revision.ItemGUID, \
                                                 revision.RevisionId, \
                                                 revision.HRID, \
                                                 revision.FolderGUID, \
                                                 revision.SourceVaultGUID)
              
                itemRevisionList.append(itemRevision)

    return itemRevisionList

def getVaultItemRevisionByItemGUID(vaultClient, itemGuidList):
    itemRevisionList = []
    itemListGroup = groupList(itemGuidList, 500)
    for itemList in itemListGroup:
        queryItemList = []  #add quotation mark for every item name to prepare for query string
        for item in itemList:
            queryItemList.append("'" + item + "'")
                 
        queryItemListStr = joinList2String(queryItemList, ",")
        if queryItemListStr:
            queryString = "ITEMGUID in (" + queryItemListStr + ")"
            try:
                vaultItemRevisionList = vaultClient.GetItemRevisions(queryString)
            except Exception, e:
                print e.Message     
                vaultItemRevisionList = ""

            for revision in vaultItemRevisionList:
                itemRevision = vaultItemRevision(revision.GUID, \
                                                 revision.Comment, \
                                                 revision.ItemGUID, \
                                                 revision.RevisionId, \
                                                 revision.HRID, \
                                                 revision.FolderGUID, \
                                                 revision.SourceVaultGUID)
              
                itemRevisionList.append(itemRevision)

    return itemRevisionList

#find the latest revision in a list
def getVaultItemRevisionInfoLatestRev(itemRevisionsList):
    #itemRevisionsList = getVaultItemRevisionInfo(vaultClient, componentOrModelList, itemType)

    #find max revID for each item revision
    revisionIdCheck = {}
    for itemRevision in itemRevisionsList:
        if revisionIdCheck.has_key(itemRevision.ItemGUID):
            if revisionIdCheck[itemRevision.ItemGUID] < itemRevision.RevisionID: 
                revisionIdCheck[itemRevision.ItemGUID] = itemRevision.RevisionID 
        else:
            revisionIdCheck[itemRevision.ItemGUID] = itemRevision.RevisionID 

    #add latest revsion into list
    itemRevisionsLatest = []
    for itemRevision in itemRevisionsList:
        if itemRevision.RevisionID == revisionIdCheck[itemRevision.ItemGUID]:
            itemRevisionsLatest.append(itemRevision)

    return itemRevisionsLatest

def getVaultModelsLinkTo(componentRevisionGUID, vaultClient):
    queryStr = "ParentItemRevisionGUID = '%s'" %componentRevisionGUID
    vaultModelLinks = vaultClient.GetItemRevisionLinks(queryStr)
    modelRevGUIDList = []
    for vaultModelLink in vaultModelLinks:
        modelRevGUIDList.append(vaultModelLink.ChildItemRevisionGUID)
    
    modelRevisionList = []
    itemListGroup = groupList(modelRevGUIDList, 500)
    for itemList in itemListGroup:
        queryItemList = [] 
        for item in itemList:
            queryItemList.append("'" + item + "'")

        queryItemListStr = joinList2String(queryItemList, ",")
        if queryItemListStr:
            queryStr = "GUID in (" + queryItemListStr + ")"
            vaultItemRevisions = vaultClient.GetItemRevisions(queryStr)

            for revision in vaultItemRevisions:
                if contentTypeDict.has_key(revision.ContentTypeGUID):
                    contentType = contentTypeDict[revision.ContentTypeGUID]       
                else:
                    contentType = None

                if contentType=="SCHLIB" or contentType=="PCBLIB":
                    itemRevision = vaultItemRevision(revision.GUID, revision.Comment, revision.ItemGUID, 
                                                     revision.RevisionId,  revision.HRID,
                                                     revision.FolderGUID, ContentType = contentType)
                    modelRevisionList.append(itemRevision)

    return modelRevisionList

def getVaultComponentRevisionsByCompoentName(componentNameList, vaultClient):
    cmpList = []
    for name in componentNameList:
        cmp = component([],[],{},"")
        cmp.parmeters["Comment"] = name
        cmpList.append(cmp)

    vaultCmpRevList = getVaultItemRevisionInfo(vaultClient, cmpList, "CMPLIB")

    return vaultCmpRevList

#the revisons reuturned by this function include component parameters
def getVaultComponentRevisionsByLinkedModelName(linkedModelNameList, modelType, vaultClient):
    modelList = []
    for modelName in linkedModelNameList:
        modelItem = model(modelName, "", "")
        modelList.append(modelItem)

    vaultCmpRevGuidList = []
    vaultModelRevList = getVaultItemRevisionInfoLatestRev(getVaultItemRevisionInfo(vaultClient, modelList, modelType))
    for modelRev in vaultModelRevList:
        queryStr = "ChildItemRevisionGUID = '%s' " %modelRev.RevisionGUID
        vaultRevisionLinks = vaultClient.GetItemRevisionLinks(queryStr)
        for link in vaultRevisionLinks:
            vaultCmpRevGuidList.append(link.ParentItemRevisionGUID )

    cmpRevisionList = []
    itemListGroup = groupList(vaultCmpRevGuidList, 500)
    for itemList in itemListGroup:
        queryItemList = [] 
        for item in itemList:
            queryItemList.append("'" + item + "'")

        queryItemListStr = joinList2String(queryItemList, ",")
        if queryItemListStr:
            queryString = "GUID in (%s)" %queryItemListStr 
            try:
                option = Altium.Sdk.DxpAppServer.VaultRequestOption.IncludeRevisionParameters
                options = Altium.Sdk.DxpAppServer.VaultRequestOptions(option)
                vaultItemRevisionList = vaultClient.GetItemRevisions(queryString, options)
            except Exception, e:
                print e.Message
                vaultItemRevisionList = ""

            for revision in vaultItemRevisionList:
                itemRevision = vaultItemRevision(revision.GUID, \
                                                 revision.Comment, \
                                                 revision.ItemGUID, \
                                                 revision.RevisionId, \
                                                 revision.HRID, \
                                                 revision.FolderGUID, \
                                                 revision.SourceVaultGUID)
                itemRevision.Description = revision.Description 

                itemRevision.RevisionsParameters = {}
                for vaultParam in revision.RevisionParameters:
                     itemRevision.RevisionsParameters[vaultParam.HRID] = vaultParam.ParameterValue 
              
                cmpRevisionList.append(itemRevision)

    cmpRevisionListLatestRev = getVaultItemRevisionInfoLatestRev(cmpRevisionList)
    return cmpRevisionListLatestRev


def getAllItemsInfoInSpecifiedFolder(vaultClient, vaultFolderGUID):
    queryString = "FOLDERGUID = '" + vaultFolderGUID + "'"
    vaultItemInfoList = vaultClient.GetItemsInfo(queryString)

    itemInfoList = []
    for info in vaultItemInfoList:
        itemInfo = vaultItemInfo(info.RevComment, info.GUID, info.HRID, info.FolderGUID, info.Description)
        itemInfoList.append(itemInfo)

    return itemInfoList

def findMaxTagIDinCMP(cmpTree):
    maxID = 0;
    for ele in cmpTree.iter():
        idTag = ele.get("id")
        if idTag:
            if int(idTag) > int(maxID):
                maxID = idTag
    return int(maxID)

def insertEle(xmlTree, newEle, path):
    isEleExiting = 0
    for newEleHRID in newEle.iter("HRID"): #this check is for modellink and rquiredParameter, there are HRIDS
        for hrid in xmlTree.iter("HRID"):
            if hrid.text == newEleHRID.text:
                isEleExiting = 1
                break

        if not isEleExiting:
            xmlTree.find(path).append(newEle)

    return isEleExiting

def createModelLinkEle(vaultItemRevision, modelType): # model type is either SCHLIB or PCBLIB
    modelLink = ET.Element("TModelLink")

    HRID = ET.SubElement(modelLink, "HRID")
    HRID.text = vaultItemRevision.HRID
    vaultGUID = ET.SubElement(modelLink, "VaultGUID")
    vaultGUID.text = vaultItemRevision.VaultGUID
    modelLink.set("id", vaultItemRevision.Comment.upper() + modelType) #this id will be replaced by real ID in later step
    itemGUID = ET.SubElement(modelLink, "ItemGUID")
    itemGUID.text = vaultItemRevision.ItemGUID
    modelKind = ET.SubElement(modelLink, "ModelKind")
    modelKind.text = modelType
    revisionGUID = ET.SubElement(modelLink, "RevisionGUID")
    revisionGUID.text = vaultItemRevision.RevisionGUID
    revisionID = ET.SubElement(modelLink, "RevisionId")
    revisionID.text = vaultItemRevision.RevisionID
    fromTemplate = ET.SubElement(modelLink, "FromTemplate")
    fromTemplate.text = "false"
    comment = ET.SubElement(modelLink, "Comment")
    comment.text = vaultItemRevision.Comment.upper()

    return modelLink

def createRequiredParamEle(paramName):
    requiredParam = ET.Element("TRequiredParameter")
    requiredParam.set("id", str(paramName)) # this will be replaced by real ID after all component
                                       # elements are inserted
    HRID = ET.SubElement(requiredParam, "HRID")
    visible = ET.SubElement(requiredParam, "Visible")
    isRequired = ET.SubElement(requiredParam, "IsRequired")
    dataType = ET.SubElement(requiredParam, "DataType")
    paramType = ET.SubElement(requiredParam, "ParamType")
    defaultValue = ET.SubElement(requiredParam, "DefaultValue")
    isReadyOnly = ET.SubElement(requiredParam, "IsReadOnly")
    HRID.text = paramName
    visible.text = "true"
    isRequired.text = "false"
    dataType.text = "Text"
    paramType.text = "4884412E-AAD1-4E69-922A-23C1C75250B1"
    defaultValue.text = ""
    isReadyOnly.text = "false"

    return requiredParam

def createModelChoiceEle(modelName, modelType):
    modelChoice = ET.Element("TModelChoice")
    requiredModel = ET.SubElement(modelChoice, "RequiredModel")
    modelLink = ET.SubElement(modelChoice, "ModelLink")
    modelLink.set("href", modelName + modelType)

    return  modelChoice

def createTparamEle(paramName, paramValue):
    tParam = ET.Element("TParameter")
    requiredParam = ET.SubElement(tParam, "RequiredParameter")
    requiredParam.set("href", paramName)
    value = ET.SubElement(tParam, "Value")
    value.text = paramValue
    realValue = ET.SubElement(tParam, "RealValue")
    realValue.text = "NaN"

    return  tParam

def initGroupEle():
    tGroup = ET.Element("TGroup")
    tGroup.set("StateIndex", 2)
    tGroup.set("Collapsed", "false")
    ET.SubElement(tGroup, "ParentGroup")
    ET.SubElement(tGroup, "Parameters")
    ET.SubElement(tGroup, "ModelChoices")
    ET.SubElement("tGroup, ComponentTypes")
    componentSet = ET.SubElement(tGroup, "ComponentSet")
    componentSet.set("href", "#0")
    ET.SubElement(tGroup, "Groups")
    ET.SubElement(tGroup, "ComponentDefinitions")
    ET.SubElement(tGroup, "Path")
    ET.SubElement(tGroup, "IsDefaultGroup")

def insertGroupEle(pathString, TopGroupsEle, allVaultFolders):
    folderGUID = getSpecificFolderGUID(pathString, allVaultFolders)
    parentGroupID = TopGroupsEle.get("id")
    pathList = pathString.split()
    foldName = pathList[len(pathList) - 1] #the folder name is in the bottom of list

    for groupsEle in TopGroupsEle.findall("./Groups"):
        hasGroupEle = 0
        for tGroupEle in groupsEle.findall(".//TGroup"):
            for guidEle in tGroupEle.iter("GUID"):
                if guidEle.text == folderGUID:
                    hasGroupEle = 1
                    groupEle = tGroupEle

        if not hasGroupEle:
            groupEle = ET.SubElement(groupsEle, "TGroup")
            groupEle.set("StateIndex", "2")
            groupEle.set("Collapsed", "false")
            groupEle.set("id", folderGUID)
            parentGroup = ET.SubElement(groupEle, "ParentGroup")
            parentGroup.set("href", "#" + parentGroupID)
            ET.SubElement(groupEle, "Parameters")
            ET.SubElement(groupEle, "ModelChoices")
            ET.SubElement(groupEle, "ComponentTypes")
            componentSet = ET.SubElement(groupEle, "ComponentSet")
            componentSet.set("href", "#0")
            ET.SubElement(groupEle, "Groups")
            ET.SubElement(groupEle, "ComponentDefinitions")
            path = ET.SubElement(groupEle, "Path")
            path.text = pathString.replace("/","\\")
            ET.SubElement(groupEle, "IsDefaultGroup")
            hrid = ET.SubElement(groupEle, "HRID")
            hrid.text = foldName
            guid = ET.SubElement(groupEle, "GUID")
            guid.text = folderGUID

    return  groupEle



def setRequiredModelID(modelEle, modelCount, modelKind):
    for requiredModel in modelEle.iter("RequiredModel"):
        if modelCount == 0:
            requiredModel.set("href", modelKind) #model kind is either PCBLIB or SCHLIB
        else:
            requiredModel.set("href", modelKind + " " + str(modelCount))

def initRequiredModelEle(modelNumber, modelKind, modelId):
    requiredModelEle = ET.Element("TRequiredModel")
    requiredModelEle.set("id", str(modelId))

    hrid = ET.SubElement(requiredModelEle, "HRID")
    hrid.text = modelKind + " " + str(modelNumber)
    visible = ET.SubElement(requiredModelEle, "Visible")
    visible.text = "true"
    modelKindEle = ET.SubElement(requiredModelEle, "ModelKind")
    modelKindEle.text = modelKind
    isRequired = ET.SubElement(requiredModelEle, "IsRequired")
    isRequired.text = "false"
    fromTemplate = ET.SubElement(requiredModelEle, "FromTemplate")
    fromTemplate.text = "false"
    isReadOnly = ET.SubElement(requiredModelEle, "IsReadOnly")
    isReadOnly.text = "false"

    return requiredModelEle

def initComponentEle():
    cmpDef = ET.Element("TComponentDefinition")
    cmpDef.set("StateIndex" , "2")

    hrid = ET.SubElement(cmpDef, "HRID")
    hrid.text = "Component0"
    ET.SubElement(cmpDef, "Parameters")
    ET.SubElement(cmpDef, "ParentGroup")
    ET.SubElement(cmpDef, "ModelChoices")
    ET.SubElement(cmpDef, "ComponentTypes")
    itemHRID = ET.SubElement(cmpDef, "ItemHRID")
    itemHRID.text = "CMP-0000"
    reservationResult = ET.SubElement(cmpDef, "ReservationResult")
    reservationResult.text = "rsReserved"

    return cmpDef

def createComponentEle(cmpHRID, symbolList, footprintList, paramDict):
    componentEle = initComponentEle()
    symbolCount = 0
    footprintCount = 0

    for hrid in componentEle.iter("HRID"):
        hrid.text = cmpHRID
    for itemHRID in componentEle.iter("ItemHRID"):
        itemHRID.text = cmpHRID

    for symbol in symbolList:
        symbolEle = createModelChoiceEle(symbol.modelName, "SCHLIB")
        setRequiredModelID(symbolEle, symbolCount, "SCHLIB")
        componentEle.find("ModelChoices").append(symbolEle)  #always insert models without check, parameters are same
        symbolCount += 1

    for footprint in footprintList:
        footprintEle = createModelChoiceEle(footprint.modelName, "PCBLIB")
        setRequiredModelID(footprintEle, footprintCount, "PCBLIB")
        componentEle.find("ModelChoices").append(footprintEle)
        footprintCount += 1

    for param in paramDict:
        paramEle = createTparamEle(param, paramDict[param])
        componentEle.find("Parameters").append(paramEle)

    return componentEle


def overwriteRequiredModelID(cmpTree):
    #overwrite existing required model id from number to text in HRID,
    # in order to prepare for rebuilding the whole cmp ID index
    for ele in cmpTree.iter("TRequiredModel"):
        for hrid in ele.iter("HRID"):
            ele.set("id", hrid.text)

    for ele in cmpTree.iter("TRequiredParameter"):
        for hrid in ele.iter("HRID"):
            ele.set("id", hrid.text)

def rebuildCMPIndex(cmpTree):
    currentID = 1
    idChangeMatch= {0:0}  #the id of root set is always 0
    overwriteRequiredModelID(cmpTree)

    for quotedEle in cmpTree.findall(".//*[@id]"):  #rebuild the index of ele which will be quoted by others
        id = quotedEle.get("id")
        if id:
            idChangeMatch[id] = currentID  #the key is the id before change, and the vaule is the ID
                                        # after change
            quotedEle.set("id", str(currentID))
            currentID += 1
    # print idChangeMatch
    for quotingEle in cmpTree.findall(".//*[@href]"): #start to change the href id
        href = quotingEle.get("href")
        if href:
            hrefID = href.replace("#", "")
            if idChangeMatch.has_key(hrefID):
                quotingEle.set("href", "#" + str(idChangeMatch[hrefID]))

    for group in cmpTree.iter("TGroup"):  #set parent group ID for every component
        groupID = group.get("id")
        for parentGroup in group.findall("./ComponentDefinitions/TComponentDefinition/ParentGroup"):
            parentGroup.set("href", "#" + groupID)

def parseTIcr(crFilePath):
    newComponentSet = componentSet([])
    newComponentSet.parmeters = {"Comment": ""}
    newComponentSet.symbolList = []
    newComponentSet.footprintList = []
    newComponentSet.tarFolderPath = []
    noParamList = ["Sim Model Name",
                   "Sim File",
                   "Sim Kind",
                   "Sim Subkind",
                   "Sim Netlist",
                   "Sim Spice Prefix",
                   "Sim Port Map",
                   "CT",
                   "CNHeader",
                   #"Comment",  #parameter Comment in CR data are set to param PartNumber, ommit Comment in process
                   "SymbolLibrary",
                   "DMS Desc",
                   "Mfr Part No",
                   "Mfg. Name"]

    #cr = open(crFilePath, "rU")
    #crDataDictList = list(csv.DictReader(cr))
    if ".csv" in crFilePath:
        crDataDictList = readCSVinOrder(crFilePath)
        removeBadCharInCrData(crDataDictList)
    elif (".xls" in crFilePath):
        crDataDictList = readExcelFile(crFilePath)
    else:
        crDataDictList = 0


    for row in crDataDictList:
        newComponent = component([],[],{}, "")
        for field in row:
            if field not in noParamList:
                if (field == "Part Number"):
                    newComponent.parmeters["Comment"] = row[field]
                    newComponent.parmeters["Part Number"] = row[field]

                if (field == "PLM Desc"):
                    newComponent.parmeters["Description"] = row[field]

                if field == "Comment" and row[field] == "=PartNumber":
                    continue

                if (field == "SymbolName") and row[field]:
                    newSymbol = model("", "", "")
                    newSymbol.modelName = row[field].upper()
                    if row.has_key("SymbolLibrary"):
                        newSymbol.libName = OP.basename(row["SymbolLibrary"]).upper()

                    if not findModelinList(row[field].upper(), newComponentSet.symbolList):
                        newComponentSet.symbolList.append(newSymbol)
                        # footprint and symbol name are converted to uppercase, so that
                        # they match the result from firebird database, because all comments are stored
                        # as uppercase strings in DB            
                    newComponent.symbolList.append(newSymbol)

                elif ("FootprintName" in field):
                    libraryField = field.replace("FootprintName", "FootprintLibrary")
                    if "Top" in libraryField:  
                        newComponent.parmeters["Top Footprint"] = row[field]
                        newComponentSet.parmeters["Top Footprint"] = row[field]
                    if "Bottom" in libraryField:  
                        newComponent.parmeters["Bottom Footprint"] = row[field]
                        newComponentSet.parmeters["Bottom Footprint"] = row[field]
                    if "Alternative" in libraryField:  
                        newComponent.parmeters["Alternative Footprint"] = row[field]
                        newComponentSet.parmeters["Alternative Footprint"] = row[field]
                                           
                    if row[field]:
                        newFootprint = model("","","")
                        newFootprint.modelName = row[field].upper()

                        
                        if row.has_key(libraryField):
                            newFootprint.libName = OP.basename(row[libraryField]).upper()

                        if not findModelinList(row[field].upper(), newComponentSet.footprintList):
                            newComponentSet.footprintList.append(newFootprint)

                        newComponent.footprintList.append(newFootprint)

                elif (field == "Vault Folder" or field == "VaultFolder") and row[field]:
                    newComponent.tarFolderPath = row[field]
                    if newComponent.tarFolderPath not in newComponentSet.tarFolderPath:
                        newComponentSet.tarFolderPath.append(newComponent.tarFolderPath)
                
                #ignore column Footprint Path, which can't be handled by noParam List
                elif "FootprintLibrary" in field: 
                    continue
                else:
                    newComponentSet.parmeters[field] = row[field]
                    if row[field]:  #only add parameters which are with value to component, but add all parameter to component set
                        newComponent.parmeters[field] = row[field]
        newComponentSet.componentList.append(newComponent)
        
    return newComponentSet

def findModelinList(modelName, modelList):
    modelFind = None
    for aModel in modelList:
        if aModel.modelName == modelName:
            modelFind = aModel
            break

    return modelFind
   

def parseAluCR(crFilePath):
    newComponentSet = componentSet([])
    newComponentSet.parmeters = {"Comment": ""}
    newComponentSet.symbolList = []
    newComponentSet.footprintList = []
    newComponentSet.tarFolderPath = []

    #cr = open(crFilePath, "rU")
    #crDataDictList = list(csv.DictReader(cr))
    if ".csv" in crFilePath:
        crDataDictList = readCSVinOrder(crFilePath)
    elif (".xls" in crFilePath):
        crDataDictList = readExcelFile(crFilePath)
    else:
        crDataDictList = 0

    #removeBadCharInCrData(crDataDictList)

    # the fields are not a part of parameters area in CR, but should be parameters in cmplib
    noParamFieldDict = {"Component Description":"Description",
                        "Manufacturer URL" : "Manufacturer URL",
                        "Manufacturer": "Manufacturer",
                        "Datasheet URL": "Datasheet URL",
                        "Datasheet Version" : "Datasheet Version",
                        "Package Reference" : "Package Reference",
                        "Package Description" : "Package Description",
                        "Package URL" : "Package URL",
                        "Package Version" : "Package Version",
                        "Component Name" : "Comment"
                        }
    for row in crDataDictList:
        newComponent = component([],[],{},"")
        for field in row:
            #print field
            if row[field]:
                if (noParamFieldDict.has_key(field)):
                    newComponent.parmeters[noParamFieldDict[field]] = row[field]
                    newComponentSet.parmeters[noParamFieldDict[field]] = row[field]

                if ("Parameter " in field):
                    paramName = row[field].partition(":")[0]
                    parmValue = row[field].partition(":")[2]
                    newComponent.parmeters[paramName] = parmValue.replace(" ", "")
                    newComponentSet.parmeters[paramName] = parmValue

                if (field == "SCH Symbol"):
                    newSymbol = model("","","")
                    newSymbol.modelName = row[field].upper()
                    if row.has_key("SCH Library"):
                        newSymbol.libName = row["SCH Library"]
                    if row.has_key("Symbol Folder"):
                        newSymbol.vaultFolder = row["Symbol Folder"]

                    if not findModelinList(row[field].upper(), newComponentSet.symbolList):                                              
                        newComponentSet.symbolList.append(newSymbol)

                    newComponent.symbolList.append(newSymbol)       

                if ("PCB Name " in field):
                    newFootprint = model("","","")
                    newFootprint.modelName = row[field].upper()

                    libraryFiled = field.replace("PCB Name", "PCB Library")
                    if row.has_key(libraryFiled):
                        newFootprint.libName = row[libraryFiled].upper()

                    if row.has_key("Footprint Folder"):
                        newFootprint.vaultFolder = row["Footprint Folder"]

                    if not findModelinList(row[field].upper(), newComponentSet.footprintList):
                        newComponentSet.footprintList.append(newFootprint)

                    newComponent.footprintList.append(newFootprint)

                if field == "Vault Folder" and row[field]:
                    newComponent.tarFolderPath = row[field]
                    if newComponent.tarFolderPath not in newComponentSet.tarFolderPath:
                        newComponentSet.tarFolderPath.append(newComponent.tarFolderPath)

        newComponentSet.componentList.append(newComponent)
    print "CR parsed"
    return newComponentSet

def writeEle2File(element, filePath):
    f = open(filePath, "wb")
    element.write(f, xml_declaration = True, encoding= "utf-8",method="xml")
    f.close()

def parseXML(filePath):
    pars = ET.XMLParser(encoding="utf-8")
    eleTree = ET.parse(filePath, parser = pars)
    return eleTree

def initCMPtree(filePath, vaultClient, componentList):
    cmpTree = parseXML(filePath)
    vaultInfo = getVaultInfo(vaultClient)
    for guid in cmpTree.iter("VaultGUID"):
        guid.text = vaultInfo["vaultGUID"]
    for name in cmpTree.iter("VaultName"):
        name.text = vaultInfo["vaultName"]

    #expand RequiredModels part in template accordoing to how much footprints does every component have
    #check each component instance, to find the max count of footprints
    maxFootprintCount = 0
    for cmp in componentList:
        if len(cmp.footprintList) > maxFootprintCount:
            maxFootprintCount = len(cmp.footprintList)
        
    requiredPCBModelCount = 0
    tagId = findMaxTagIDinCMP(cmpTree) + 1
    if maxFootprintCount > 1:
        for i in xrange(1, maxFootprintCount):
            tRequiredModelEle = initRequiredModelEle(i, "PCBLIB", tagId)
            insertEle(cmpTree, tRequiredModelEle, "RequiredModels")
    #for requiredModelEle in cmpTree.iter("TRequiredModel"): 
    #    for hridEle in requiredModelEle.iter("HRID"):
    #        if "PCBLIB" in hridEle.text:
    #            requiredPCBModelCount += 1

    return  cmpTree

def prettify(xmlTree):
    """Return a pretty-printed XML string for the Element.
    """
    for ele in xmlTree.findall("."):
        rough_string = ET.tostring(ele, 'utf-8')
    reparsed = MD.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def readCSV(filePath):
    cr = open(filePath, "rU")
    crDataDictList = list(csv.DictReader(cr))

    return crDataDictList

def readCSVinOrder(filePath):
    csvFile = open(filePath, "rU")
    sourceData = csv.reader(csvFile)

    dataDictList = []
    for rowNumber, row in enumerate(sourceData):
        if rowNumber == 0:
            headers = row
        else:
            dataDict = OrderedDict()
            for i in xrange(len(row)):
                dataDict[headers[i]] = row[i]
            dataDictList.append(dataDict)
            #print dataDict.items()

    return dataDictList
           

def writeDict2CSV(filePath, dataDictList):  
    headers = []
    for row in dataDictList:
        for key in row:
            if key not in headers:
                headers.append(key)

    csvFile = open(filePath, "wb")
    writer = csv.DictWriter(csvFile, headers)
    writer.writeheader()
    for i in dataDictList:
        try:
            writer.writerow(i)
        except Exception, e:
            print e.Message

def readExcelFile(filePath):
    try:
        data = xlrd.open_workbook(filePath)
    except Exception, e:
        print str(e)

    table = data.sheets()[0]
    rowCount = table.nrows
    colCount = table.ncols
    headers = table.row_values(0)

    dataList = []
    for rowIndex in xrange(1, rowCount):
        row = table.row_values(rowIndex)
        if row:
            rowDataDict = OrderedDict()
            #rowDataDict = {}
            for i in xrange(len(headers)):
                if type(row[i]) == float: #porcess int value as string
                    if int(row[i]) == row[i]:
                        row[i] = int(row[i])

                rowDataDict[headers[i]] =str(row[i])

            dataList.append(rowDataDict)

    return dataList

def writeDict2Excel(filePath, dataDictList):
    headers = []
    for row in dataDictList:
        for key in row:
            if key not in headers:
                headers.append(key)

    wb = xlwt.Workbook(encoding = 'utf8')
    ws = wb.add_sheet(os.path.basename(filePath).rpartition(".")[0])
    for i in xrange(len(headers)):
        ws.write(0, i, headers[i])

    for i in xrange(len(dataDictList)):
        for j in xrange(len(headers)):
            if dataDictList[i].has_key(headers[j]):
                    ws.write(i + 1, j, dataDictList[i][headers[j]])

    wb.save(filePath)


def readRecord(filePath):
    if ".csv" in filePath:
        data = readCSV(filePath)
    elif ".xls" in filePath:
        data = readExcelFile(filePath)
    else: data = ""

    return data

def copyFile(fileName, tarPath, srcPath, replaceFile): #path like C:\\OS\\Copy
    fileCopied = 0
    absTarFilePath = OP.join(tarPath, fileName)
    absSrcFilePath = OP.join(srcPath, fileName)
    if OP.isfile(absSrcFilePath) and OP.isdir(srcPath):
        if not (not replaceFile and OP.isfile(absTarFilePath)):
            shutil.copyfile(absSrcFilePath, absTarFilePath)
            fileCopied =1

    return fileCopied

def getItemInfoinSpeificFolder(folderPath, vaultClient, allVaultFolders):
    #itemList = []
    #folderGUID = getSpecificFolderGUID(folderPath, allVaultFolders)
    ##queryString = "select REVCOMMENT, GUID, HRID from ALU_ITEMINFO " \
    ##              "where FOLDERGUID = '" + folderGUID + "';"
    #queryString = "REVCOMMENT like '%' and FOLDERGUID = '" + folderGUID + "'"
    
    #client = vaultClient
    #itemInfoList = client.GetItemsInfo(queryString)
    #for item in itemInfoList:
    #    itemAttr = []
    #    itemAttr.append(item.RevComment.upper())
    #    itemAttr.append(item.GUID)
    #    itemAttr.append(item.HRID)
    #    itemList.append(itemAttr)

    #return itemList

    folderGUID =  getSpecificFolderGUID(folderPath, allVaultFolders)              
    queryString = "FOLDERGUID ='" + folderGUID + "'"
    vaultItemRevisionList = vaultClient.GetItemRevisions(queryString)

    itemRevisionList = []
    for revision in vaultItemRevisionList:
        itemRevision = vaultItemRevision(revision.GUID, \
                                         revision.Comment, \
                                         revision.ItemGUID, \
                                         revision.RevisionId, \
                                         revision.HRID, \
                                         revision.FolderGUID, \
                                         revision.SourceVaultGUID)
              
        itemRevisionList.append(itemRevision)

    return itemRevisionList



class progressbarClass:
    def __init__(self, finalcount, progresschar=None):
        import sys
        self.finalcount=finalcount
        self.blockcount=0
        #
        # See if caller passed me a character to use on the
        # progress bar (like "*").  If not use the block
        # character that makes it look like a real progress
        # bar.
        #
        if not progresschar: self.block=chr(178)
        else:                self.block=progresschar
        #
        # Get pointer to sys.stdout so I can use the write/flush
        # methods to display the progress bar.
        #
        self.f=sys.stdout
        #
        # If the final count is zero, don't start the progress gauge
        #
        if not self.finalcount : return
        self.f.write('\n------------------- % Progress -------------------\n')
        return

    def progress(self, count):
        #
        # Make sure I don't try to go off the end (e.g. >100%)
        #
        count=min(count, self.finalcount)
        #
        # If finalcount is zero, I'm done
        #
        if self.finalcount:
            percentcomplete=int(round(100*count/self.finalcount))
            if percentcomplete < 1: percentcomplete=1
        else:
            percentcomplete=100

        #print "percentcomplete=",percentcomplete
        blockcount=int(percentcomplete/2)
        #print "blockcount=",blockcount
        if blockcount > self.blockcount:
            for i in range(self.blockcount,blockcount):
                self.f.write(self.block)
                self.f.flush()

        if percentcomplete == 100: self.f.write("\n")
        self.blockcount=blockcount
        return

class progressCount:
    def __init__(self, finalCount, promptText = ""):
        self.finalCount = finalCount
        self.blockCount = 0
        self.f = sys.stdout
        
    def progress(self,count):
        count = min(count, self.finalCount)
        if self.finalCount:
            precentComplete = int(round(100*count/self.finalCount))
            if precentComplete < 1:
                precentComplete = 1
        else:
            precentComplete = 100
        
        if precentComplete > (self.blockCount + 1):
            self.f.write(self.promptText + " " + precentComplete + "%...")
            self.f.flush()

        if precentComplete == 100:
            self.f.write("\n")

        self.blockCount = precentComplete
    

def getCmpTypeGUID(ComponentTypeName):
    queryString = "select GUID from ALU_TAG where HRID ='" + ComponentTypeName + "';"
    cursor = initDBConnection()
    cursor.execute(queryString)
    for id in cursor.fetchone():
        HRID = id

    return HRID

def createCMPTypeEle(typeName,typeGUID):
    cmpTypeEle = ET.Element("ComponentTypes")
    hridEle = ET.SubElement(cmpTypeEle, "HRID")
    hridEle.text = typeName
    valueEle = ET.SubElement(cmpTypeEle, "Value")
    valueEle.text = typeGUID

    return cmpTypeEle

def getComponetParamValue(componentEle, paramName, cmpTree):
    paramValue = ""
    paramID = ""

    for requiredEle in cmpTree.iter("TRequiredParameter"):
        for hridEle in requiredEle.iter("HRID"):
            if hridEle.text == paramName:
                paramID = requiredEle.get("id")

        if paramID:
            for paramEle in componentEle.iter("TParameter"):
                for requiredParamEle in paramEle.iter("RequiredParameter"):
                    if requiredParamEle.get("href") == ("#" + paramID):
                        for valueEle in paramEle.iter("Value"):
                            paramValue = valueEle.text

    return paramValue

#def cleanCash():
#    if OP.isfile("vaultFolder.xml"):
#        os.remove("vaultFolder.xml")

def removeBadCharInCrData(crData):
    for row in crData:
        for field in row:
            try:
                row[field].decode("utf_8")
            except Exception, ex:
                print row[field] + " invalid"
                row[field] = "Error!"

#def getModelsinCR(crContent, crType, modelType):
#    modelDict = {}
#    if crType == "Altium":
#        symHeaderDict = {"SCH Library":"SCH Symbol"}
#        fpHeaderDict = {"PCB Library 1":"PCB Name 1",
#                         "PCB Library 2":"PCB Name 2",
#                         "PCB Library 3":"PCB Name 3"}
#    else:
#        fpHeaderDict = {"Footprint Path":"Footprint Ref",
#                      "Footprint Path 2":"Footprint Ref 2",
#                      "Footprint Path 3":"Footprint Ref 3",
#                      "Footprint Path 4":"Footprint Ref 4",
#                      "Footprint Path 5":"Footprint Ref 5",}
#        symHeaderDict = {"Library Path":"Library Ref"}

#    if modelType == "SCHLIB":
#        headerDict = symHeaderDict
#    else: headerDict = fpHeaderDict

#    for row in crContent:
#        for field in row:
#            if headerDict.has_key(field) and row[field]:
#                modelFileName = row[field].upper()
#                if crType != "Altium":  #process TI style record
#                    modelFileName = OP.basename(modelFileName).upper()
                                                    
#                modelDict[row[headerDict[field]].upper()]= modelFileName  #key is model name, value is model file name

#    return  modelDict


def removeVaultIteminDict(itemDict, vaultFolder, vaultClient, vaultFolders):
    #check the dictionary and vault, remove the items has been in vault
    itemsinSpecificFolder = []
    itemList = getItemInfoinSpeificFolder(vaultFolder, vaultClient, vaultFolders)
    for i in itemList:
        itemsinSpecificFolder.append(i.Comment.upper())
    
    #remove items which have been in vault folder from dict
    removeList = []
    for model in itemDict:
        if model in itemsinSpecificFolder:
            removeList.append(model)
    for i in removeList:
        del itemDict[i]


#def copyModels(locationInfo, vaultCredential):
#    crData = readCSV(locationInfo["crPath"])
#    client = initVaultConnection(vaultCredential["vault address"], vaultCredential["user name"], vaultCredential["password"])
#    allFolders = getVaultFolders(client)

#    modelDict = getModelsinCR(crData, locationInfo["crType"], "SCHLIB")
#    removeVaultIteminDict(modelDict, locationInfo["symVaultFolder"], client, allFolders)
#    #start to copy files
#    for model in modelDict:
#        isCopied = copyFile(modelDict[model], locationInfo["tarFolderPath"], locationInfo["symSrcFolderPath"], 0)
#        if isCopied:
#            print model + " copied"

#    modelDict = getModelsinCR(crData, locationInfo["crType"], "PCBLIB")
#    removeVaultIteminDict(modelDict, locationInfo["fpVaultFolder"], client, allFolders)
#    for model in modelDict:
#        isCopied = copyFile(modelDict[model], locationInfo["tarFolderPath"], locationInfo["fpSrcFolderPath"], 0)
#        if isCopied:
#            print model + " copied"

def moveItem(itemGUID, folderGUID, vaultClient):
        move = VaultSDK.VaultMoveItem(itemGUID, folderGUID)
        vaultClient.MoveItem(move)

def moveItems(itemTarFolderDict, vaultClient):
    if itemTarFolderDict:
        moveCollection = VaultSDK.VaultMoveItemList()
        for itemGUID in itemTarFolderDict:
            move = VaultSDK.VaultMoveItem(itemGUID, itemTarFolderDict[itemGUID])
            moveCollection.Add(move)

        vaultClient.MoveItems(moveCollection)

def initCiivaConnection():
    ciivaClient = ciivaAPI.GetApiClient()

    return ciivaClient

def ciivaGetSupplierComponentsBySPN(supplierName, supplierPartNumber, apiClient):
    ciivaAPI.GetSupplierComponentsByPartNumber(supplierName, supplierPartNumber, apiClient)

    result = json.loads(ciivaAPI.queryResult)
    return result

def ciivaGetManufacturerComponentByPartNumber(manufacturerName, manufacturerPartnumber, apiClient):
    ciivaAPI.GetManufacturerComponentsByPartNumberRequest(manufacturerName, manufacturerPartnumber, apiClient)
    result = json.loads(ciivaAPI.queryResult)

    return result

def ciivaGetManufacturerComponentById(manufacturerComponentId, apiClient):
    ciivaAPI.GetManufacturerComponentById(manufacturerComponentId, apiClient)
    result = json.loads(ciivaAPI.queryResult)

    return result

def traversalFolder(path, fileExtension):
    allFiles = os.walk(path)

    filesList = []
    for root, dirs, files in allFiles:
        for fileName in files:
            fullName = root + "\\" + fileName
            if fileExtension in fullName:
                filesList.append(fullName)

    return filesList

def createVaultFolder(folderPath, allFolders, vaultClient):
    if "\\" in folderPath:
        pathList = folderPath.split("\\")
    else:
        pathList = folderPath.split("/")

    path = ""
    for i in xrange(len(pathList)):
        path = path + pathList[i]
        if not getSpecificFolderGUID(path, allFolders):     
            try:              
                aVaultFolder = vaultClient.AddFolder(VaultSDK.FolderTypeGuid.ComponentLibrary, path)
                newFolder = vaultFolder(aVaultFolder.GUID, aVaultFolder.ParentFolderGUID, aVaultFolder.HRID, 0, 0)
                #newFolder.folderName = aVaultFolder.HRID
                #newFolder.guid = aVaultFolder.GUID
                #newFolder.parentFolderGUID = aVaultFolder.ParentFolderGUID
                allFolders.append(newFolder)
            except Exception, e:
                print e

        path = path + "\\"

def findNextLifeCycleStateByGUID(currentLifeCycleStateGUID, vaultClient):
    queryString = " LifeCycleStateBeforeGUID = '%s'" % currentLifeCycleStateGUID
    stateTransitionsList = vaultClient.GetLifeCycleStateTransitions(queryString)
    nextStateGUIDList = []
    for stateTransition in stateTransitionsList:
        nextStateGUIDList.append(stateTransition.LifeCycleStateAfterGUID)

def findLifeCycleStateTransistionsByGUID(currentLifeCycleStateGUID, vaultClient):
    queryString = " LifeCycleStateBeforeGUID = '%s'" % currentLifeCycleStateGUID
    stateTransitionsList = vaultClient.GetLifeCycleStateTransitions(queryString)
    
    return stateTransitionsList

def updateLifeCycleChange(vaultItemRevision, lifeCycleTransitionGUID, vaultClient):
    lifeCycleChange = VaultSDK.VaultLifeCycleStateChange(vaultItemRevision.GUID, lifeCycleTransitionGUID)
    vaultClient.AddLifeCycleStateChange(lifeCycleChange)
    vaultItemRevision.StateChanges.append(lifeCycleChange)

    return vaultItemRevision

def pushLifeCycleStateToNext(vaultItemRevision, vaultClient):
    stateTransitionsList = findLifeCycleStateTransistionsByGUID(vaultItemRevision.LifeCycleStateGUID, vaultClient)
    if stateTransitionsList.Count > 1:
        stateNameList = []
        for stateTransition in stateTransitionsList:
            sateName = vaultClient.GetLifeCycleStateByGuid(stateTransition.LifeCycleStateAfterGUID).HRID
            stateNameList.append(sateName)
        index = selectItemInList(stateNameList)
        stateTransition = stateTransitionsList[index]

    else:
        stateTransition = stateTransitionsList[0]

    vaultItemRevision.LifeCycleStateGUID = stateTransition.LifeCycleStateAfterGUID
    #vaultClient.UpdateItemRevision(vaultItemRevision)   #no need to update item revision
    lifeCycleChange = VaultSDK.VaultLifeCycleStateChange(vaultItemRevision.GUID, stateTransition.GUID,True)
    vaultClient.AddLifeCycleStateChange(lifeCycleChange)

def retriveItemHRID(itemNamingScheme, initialIndex, vaultClient, HRIDCount, itemType):
    newHRIDList = []
    if ("{" in itemNamingScheme) and ("}" in itemNamingScheme):
        numberScheme = itemNamingScheme.rpartition("{")[2].rpartition("}")[0]
        if numberScheme.isdigit():
            if len(numberScheme) >= len(initialIndex):
                newIndex = "0" * (len(numberScheme) - len(initialIndex)) + initialIndex
                newScheme = itemNamingScheme.rpartition("{")[0] + newIndex + itemNamingScheme.rpartition("}")[2]

                if itemType == "SCHLIB":
                    itemTypeGUID = VaultSDK.ContentTypeGuid.cSymbol
                elif itemType == "PCBLIB":
                    itemTypeGUID = VaultSDK.ContentTypeGuid.PcbComponent
                elif itemType == "CMP":
                    itemTypeGUID = VaultSDK.ContentTypeGuid.cComponent
                else:
                    itemTypeGUID = ""
                queryString = "HRID > '" + newScheme + "' AND CONTENTTYPEGUID = '" + itemTypeGUID + "'"
                vaultItemList = vaultClient.GetItems(queryString)

                existingHRIDList = []
                for vaultItem in vaultItemList:
                    if itemType in vaultItem.HRID:
                        existingHRIDList.append(vaultItem.HRID)
                if existingHRIDList:
                    maxHRID = 0
                    for id in existingHRIDList:
                        idNumber = id.replace(itemNamingScheme.rpartition("{")[0], "").replace(itemNamingScheme.rpartition("}")[2], "")
                        if idNumber.isdigit():
                            if int(idNumber) > maxHRID:
                                maxHRID = int(idNumber)
                    #x = max(existingHRIDList).replace(itemNamingScheme.rpartition("{")[0], "").replace(itemNamingScheme.rpartition("}")[2], "")
                    #maxHRID = int(max(existingHRIDList).replace(itemNamingScheme.rpartition("{")[0], "").replace(itemNamingScheme.rpartition("}")[2], ""))
                else: maxHRID = int(initialIndex)
                
                for i in xrange(1, HRIDCount + 1):
                    maxHRID = maxHRID + 1
                    newIndex = "0" * (len(numberScheme) - len(str(maxHRID))) + str(maxHRID)
                    newHRIDList.append(itemNamingScheme.rpartition("{")[0] + newIndex + itemNamingScheme.rpartition("}")[2])

        return newHRIDList

def selectItemInList(aList):
    for item in xrange(len(aList)):
        print "[%s] %s" %(item + 1, aList[item]) 

    print ""
    index = raw_input()
    validIndex = 0
    if index.isdigit():
        if int(index) <= len(aList) and int(index) > 0:
            validIndex = int(index)
    while not validIndex:
        print "input index is not valid"
        index = raw_input()
        if index.isdigit():
            if int(index) <= len(aList) and int(index) > 0:
                validIndex = int(index)

    return validIndex - 1


def groupList(aList, maxNumberInList):
   batchNumber = len(aList) //maxNumberInList + 1

   listGroup = []
   if batchNumber == 1:
       listGroup.append(aList)
   else:
       for i in xrange(batchNumber):
           sliceList = aList[(i*maxNumberInList) : ((i + 1)* maxNumberInList)]
           listGroup.append(sliceList)
   return listGroup
