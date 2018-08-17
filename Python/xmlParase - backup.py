import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import csv
import os


workPath = "G:\Project Documents\TI package code change\CmpLibs and Modified Record\TI"
fileCollection = os.walk(workPath)
vaultIDLib = ET.parse(workPath + "\\vaultIDLib.CmpLib")

def copyLinkedModel(model):
    newModel = ET.Element("TModelLink")
    newModel.set("id", "1")
    
    for item in model:
        newItem = ET.SubElement(newModel,item.tag)
        newItem.text = item.text
##        ET.dump(newItem)

##    ET.dump(newModel)
    return newModel

for root, dirs, files in fileCollection:
    for csvName in files:
        if ".csv" in csvName:
            hridList = []
            CR = open(root + "\\" + csvName, "rU")
            crDataDict = list(csv.DictReader(CR))
            for rowData in crDataDict:
                if (rowData["PCBLIB 1"] not in hridList) and rowData["PCBLIB 1"] != "":
                    hridList.append(rowData["PCBLIB 1"])
                if (rowData["PCBLIB 2"] not in hridList) and rowData["PCBLIB 2"] != "":
                    hridList.append(rowData["PCBLIB 2"])
                if (rowData["PCBLIB 3"] not in hridList) and rowData["PCBLIB 3"] != "":
                    hridList.append(rowData["PCBLIB 3"])
            CR.close
            
            cmpLibFileName = csvName.replace(".csv", ".CmpLib")
            cmpLibFileName = cmpLibFileName.replace("[Modified]", "")
            if os.path.isfile(workPath + "\\" + cmpLibFileName):
                modelTree = ET.parse(workPath + "\\" + cmpLibFileName)
                for hrid in hridList:
                    hridFound = False
                    for linkedModel in vaultIDLib.iter("TModelLink"):
                        for hridEle in linkedModel.iter("HRID"):
                            if hridEle.text == hrid:
                                hridFound = True
                                break
                        if hridFound:
                            cloneModel = copyLinkedModel(linkedModel)
                            modelTree.find("./ModelLinks").append(cloneModel)
        
##                ET.dump(modelTree)
##                ts = ET.tostring(modelTree.getroot(), encoding="utf-8", method="xml")
##                domTree = parseString(ts)

                i = 0
                for ele in modelTree.iter():
                    idTag = ele.get("id")
                    if idTag:
                        ele.set("id", str(i))
                        i= i + 1
##                ET.dump(modelTree)

                f = open("[Modified]" + cmpLibFileName, "wb")
##                domTree.writexml(f,  addindent = ' ' , newl = '\n' ,encoding = 'utf-8')

                modelTree.write(f, xml_declaration = True, encoding= "utf-8",method="xml")
                f.close()
            else:
                print cmpLibFileName + " is not existed"
            

##DOMTree = parse("G:\\TestArea\\test cmp.CmpLib")
##collection = DOMTree.documentElement
##
##linkedModels = collection.getElementsByTagName("ModelLinks")
##nodeID5 = collection.getElementsByTagName("TModelLink")[0]
##newItem = nodeID5.cloneNode(True)
##linkedModels[0].appendChild(newItem)
##
####model = DOMTree.createElement("TModelLink")
####linkedModels[0].appendChild(model)
####TModel = DOMTree.createElement("HRID")
####TModelText = DOMTree.createTextNode("PCC-000-0000000")
####TModel.appendChild(TModelText)
####model.appendChild(TModel)
##
##f = open('G:\\TestArea\\testResult.cmplib', 'w')
##DOMTree.writexml(f)
##f.close()
##linkedModels = collection.getElementsByTagName("TModelLink")
##for model in linkedModels:
##    HRID = model.getElementsByTagName("HRID")[0]
##    print HRID.childNodes[0].nodeValue

