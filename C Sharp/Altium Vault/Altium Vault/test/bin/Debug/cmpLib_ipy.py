import csv
import os
import os.path as OP
import shutil
import xml.etree.ElementTree as ET
import clr
from System import *
clr.AddReferenceToFileAndPath("D:\\Vault SDK\\bin\\DxpServerSDK.dll")
import Altium.Sdk.DxpAppServer as VaultSDK



class vaultItemRevision:
    def __init__(self, RevisionGUID, Comment, ItemGUID, RevisionID, HRID, vaultGUID):
        self.RevisionGUID = RevisionGUID
        self.Comment = Comment
        self.ItemGUID = ItemGUID
        self.RevisionID = RevisionID
        self.HRID = HRID
        self.vaultGUID = vaultGUID

class component:
    symbolList = []
    footprintList = []
    parmeters = {}
    tarFolderPath = ""
    def __init__(self, symbolList, footprintList, parmeters, tarFolderPath):
        self.symbolList = symbolList
        self.footprintList = footprintList
        self.parmeters = parmeters  #dict
        self.tarFolderPath = tarFolderPath

class componentSet(component):
    def __init__(self, componentList):
        self.componentList = componentList

def initVaultConnection(vaultAddress, username, passowrd):
    if (vaultAddress == 'http://vault.live.altium.com'):
        loginURL = 'http://ids.live.altium.com/?cls=soap'
        serviceURL = 'http://vault.live.altium.com/?cls=soap'
    else:
        loginURL = vaultAddress + "/ids/?cls=soap"
        serviceURL = vaultAddress + "/vault/?cls=soap"

    idsClient = VaultSDK.IDSClient(loginURL)
    loginResult = idsClient.Login(username, passowrd, False)
    vaultClient = VaultSDK.VaultClient(serviceURL)
    vaultClient.Login(loginResult.SessionId)

    return vaultClient

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

    vaultFolders = {}
    for folder in folderList:
        folderAttr = {}
        folderAttr["Folder Name"] = folder.HRID
        folderAttr["Parent Folder"] = folder.ParentFolderGUID
        vaultFolders[folder.GUID] = folderAttr  #folder GUID is key
    
    return vaultFolders

def buildFolderTree(vaultClient):
    client = vaultClient
    vaultFolders = getVaultFolders(client)
    tree = ET.ElementTree()
    treeEle = ET.Element("FolderSet")
    tree._setroot(treeEle)
    nodeList = []
    badCharList = [" ", "&"]
    for folderItem in vaultFolders:
        folderName = "a" + vaultFolders[folderItem]["Folder Name"]  #avoid the folder name start with number or symbol
        for char in badCharList: #remove bad characters that XML doesn't support
            folderName = folderName.replace(char, "")
        currentNode = ET.Element(folderName)
        currentNode.set("GUID", folderItem)
        if not vaultFolders[folderItem]["Parent Folder"]:
            treeEle.append(currentNode)
        else:
            currentNode.set("Parent", vaultFolders[folderItem]["Parent Folder"])
            nodeList.append(currentNode)

    while nodeList:
        for currentNode in nodeList:
            parentFound = 0
            for node in treeEle.findall(".//"):       
                if node.get("GUID") == currentNode.get("Parent"):
                    node.append(currentNode)
                    nodeList.remove(currentNode)
                    parentFound = 1
                    break;
            if parentFound: break
   
    writeEle2File(tree, "vaultFolder.xml")
   
    return treeEle

def getSpecificFolderGUID(folderPath, *vaultClient):
    if not OP.isfile("vaultFolder.xml"):
        buildFolderTree(vaultClient[0])
    folderTree = ET.parse("vaultFolder.xml")

    badCharList = [" ", "&"]
    for char in badCharList:
        folderPath = folderPath.replace(char, "")
    folderPath = folderPath.replace("/", "/a")
    folderPath = "./a" + folderPath
    folderEle = folderTree.find(folderPath)
    folderGUID = ""
    if folderEle != None:
        folderGUID = folderEle.get("GUID")

    return folderGUID

def getBatchVaultItemInfofromVault(vaultClient, itemNameList, *folderPath):
    client = vaultClient
    queryItemList = []  #add quotation mark for every item name to prepare for query string
    for name in itemNameList:
        queryItemList.append("'" + name + "'")

    if folderPath: #if folderpath is required
        specifiedFolderGUID = getSpecificFolderGUID(folderPath[0], client)
        queryString = "COMMENT in (" + joinList2String(queryItemList, ",") + ") and FOLDERGUID = '" + specifiedFolderGUID + "'"
        
    else:
        queryString = "COMMENT in (" + joinList2String(queryItemList, ",") + ")"

        print queryString
        vaultItemRevisionList = client.GetItemRevisions(queryString)

    itemRevisionList = []
    for revision in vaultItemRevisionList:
        itemRevision = vaultItemRevision(revision.GUID, \
                                         revision.Comment, \
                                         revision.ItemGUID, \
                                         revision.RevisionId, \
                                         revision.HRID, \
                                         revision.SourceVaultGUID)
        itemRevisionList.append(itemRevision)


    return itemRevisionList

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
    vaultGUID.text = vaultItemRevision.vaultGUID
    modelLink.set("id", vaultItemRevision.Comment.upper()) #this id will be replaced by real ID in later step
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

def createModelChoiceEle(modelName):
    modelChoice = ET.Element("TModelChoice")
    requiredModel = ET.SubElement(modelChoice, "RequiredModel")
    modelLink = ET.SubElement(modelChoice, "ModelLink")
    modelLink.set("href", modelName)

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

def insertGroupEle(pathString, TopGroupsEle, vaultClient):
    folderGUID = getSpecificFolderGUID(pathString, vaultClient)
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
        symbolEle = createModelChoiceEle(symbol)
        setRequiredModelID(symbolEle, symbolCount, "SCHLIB")
        componentEle.find("ModelChoices").append(symbolEle)  #always insert models without check, parameters are same
        symbolCount += 1

    for footprint in footprintList:
        footprintEle = createModelChoiceEle(footprint)
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
    noParamList = ["Sim Model Name",
                   "Sim File",
                   "Sim Kind",
                   "Sim Subkind",
                   "Sim Netlist",
                   "Sim Spice Prefix",
                   "Sim Port Map",
                   "Footprint Path",
                   "Footprint Path 2",
                   "Footprint Path 3",
                   "Footprint Path 4",
                   "Footprint Path 5",
                   "Library Path"]

    cr = open(crFilePath, "rU")
    crDataDictList = list(csv.DictReader(cr))

    for row in crDataDictList:
        newComponent = component([],[],{}, "")
        for field in row:
            if not field in noParamList:
                if (field == "PartNumber"):
                    newComponent.parmeters["Comment"] = row[field]
                if (field == "Library Ref") and row[field]:
                    if row[field].upper() not in newComponentSet.symbolList:
                        # footprint and symbol name are converted to uppercase, so that
                        # they match the result from firebird database, because all comments are stored
                        # as uppercase strings in DB
                        newComponentSet.symbolList.append(row[field].upper())
                    newComponent.symbolList.append(row[field].upper())
                elif ("Footprint Ref" in field) and row[field]:
                    if row[field].upper() not in newComponentSet.footprintList:
                        newComponentSet.footprintList.append(row[field].upper())
                    newComponent.footprintList.append(row[field].upper())

                elif field == "Vault Folder" and row[field]:
                    newComponent.tarFolderPath = row[field]

                elif ("Footprint Ref" in field):
                    continue
                else:
                    newComponentSet.parmeters[field] = row[field]
                    if row[field]:  #only add parameters which are with valut to component, but add all parameter to component set
                        newComponent.parmeters[field] = row[field]
        newComponentSet.componentList.append(newComponent)

    return newComponentSet

def parseAluCR(crFilePath):
    newComponentSet = componentSet([])
    newComponentSet.parmeters = {"Comment": ""}
    newComponentSet.symbolList = []
    newComponentSet.footprintList = []

    cr = open(crFilePath, "rU")
    crDataDictList = list(csv.DictReader(cr))

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
                    if row[field].upper() not in newComponentSet.symbolList:
                        newComponentSet.symbolList.append(row[field].upper())
                    newComponent.symbolList.append(row[field].upper())

                if ("PCB Name " in field):
                    if row[field].upper() not in newComponentSet.footprintList:
                        newComponentSet.footprintList.append(row[field].upper())
                    newComponent.footprintList.append(row[field].upper())

                if field == "Vault Folder" and row[field]:
                    newComponent.tarFolderPath = row[field]

        newComponentSet.componentList.append(newComponent)

    return newComponentSet

def writeEle2File(element, filePath):
    f = open(filePath, "wb")
    element.write(f, xml_declaration = True, encoding= "utf-8",method="xml")
    f.close()

def parseXML(filePath):
    eleTree = ET.parse(filePath)
    return eleTree

def initCMPtree(filePath, vaultClient):
    cmpTree = parseXML(filePath)
    vaultInfo = getVaultInfo(vaultClient)
    for guid in cmpTree.iter("VaultGUID"):
        guid.text = vaultInfo["vaultGUID"]
    for name in cmpTree.iter("VaultName"):
        name.text = vaultInfo["vaultName"]

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

def copyFile(fileName, tarPath, srcPath, replaceFile): #path like C:\\OS\\Copy
    fileCopied = 0
    absTarFilePath = OP.join(tarPath, fileName)
    absSrcFilePath = OP.join(srcPath, fileName)
    if OP.isfile(absSrcFilePath) and OP.isdir(srcPath):
        if not (not replaceFile and OP.isfile(absTarFilePath)):
            shutil.copyfile(absSrcFilePath, absTarFilePath)
            fileCopied =1

    return fileCopied

def getItemInfoinSpeificFolder(folderPath, vaultClient):
    itemList = []
    folderGUID = getSpecificFolderGUID(folderPath, vaultClient)
    #queryString = "select REVCOMMENT, GUID, HRID from ALU_ITEMINFO " \
    #              "where FOLDERGUID = '" + folderGUID + "';"
    queryString = "REVCOMMENT like '%' and FOLDERGUID = '" + folderGUID + "'"
    
    client = vaultClient
    itemInfoList = client.GetItemsInfo(queryString)
    for item in itemInfoList:
        itemAttr = []
        itemAttr.append(item.RevComment)
        itemAttr.append(item.GUID)
        itemAttr.append(item.HRID)
        itemList.append(itemAttr)

    return itemList



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

def cleanCash():
    if OP.isfile("vaultFolder.xml"):
        os.remove("vaultFolder.xml")

def buildCmpLib(crPath, cmpLibPath, crType, vaultAddress, userName, pwd):
    cleanCash()
    print "start to init connection"

    client = initVaultConnection(vaultAddress, userName, pwd)

    print "init template"

    cmpEleTree = initCMPtree("Template.CmpLib", client)
    if (crType == "Altium"):
        componentSet = parseAluCR(crPath)
    else:
        componentSet = parseTIcr(crPath)

    #query the data of models in DB, get item revision guid. Can check models from given folders
    #if tarSymbolVaultFolder and tarFootprintVaultFolder:
     #   symbolVaultItemList = getBatchVaultItemInfofromVault(componentSet.symbolList, tarSymbolVaultFolder)
      #  footprintVaultItemList = getBatchVaultItemInfofromVault(componentSet.footprintList, tarFootprintVaultFolder)
    #else:
     #   symbolVaultItemList = getBatchVaultItemInfofromVault(componentSet.symbolList)
      #  footprintVaultItemList = getBatchVaultItemInfofromVault(componentSet.footprintList)

    print "get vault item revisions"

    symbolVaultItemList = getBatchVaultItemInfofromVault(client, componentSet.symbolList)
    footprintVaultItemList = getBatchVaultItemInfofromVault(client, componentSet.footprintList)
    
    print "insert components"
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
    componentCount = 0
    for component in componentSet.componentList:
        componentHRID = "CMP-0000" + str(componentCount)
        componentEle = createComponentEle(componentHRID,component.symbolList, component.footprintList, component.parmeters)
        vaultFolderGUID = getSpecificFolderGUID(component.tarFolderPath, client)
        if not vaultFolderGUID:
            insertEle(cmpEleTree, componentEle, "./TopGroup/Groups/TGroup/ComponentDefinitions")
        else:
            for topGroup in cmpEleTree.findall("./TopGroup"):
                tGroup = insertGroupEle(component.tarFolderPath, topGroup, client)
                insertEle(tGroup, componentEle, "ComponentDefinitions")
   
        componentCount += 1
    
    print "write reulst " + cmpLibPath 
    print cmpLibPath

    rebuildCMPIndex(cmpEleTree)
    writeEle2File(cmpEleTree, cmpLibPath)
