from cmpLib_ipy import *

config = configInfo()
config.readConfigFile("Config.ini")
crPath = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]
 
if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)

ciivaClient = initCiivaConnection()
ciivaCmpParamsDict = {}
#pb = progressbarClass(len(componentSet.componentList), "*")
componentCount = 0
for cmp in componentSet.componentList:
    progressStr = "%s / %s..." %(str(componentCount), str(len(componentSet.componentList)))
    sys.stdout.writelines(progressStr + "\r")
    sys.stdout.flush()

    if cmp.parmeters.has_key("Comment"):
        ciivaCmpParamsDict[cmp.parmeters["Comment"]] = {}   #create a new space to restore ciiva parameters for each cmp
        if cmp.parmeters.has_key("Manufacturer"):
            result = ciivaGetManufacturerComponentByPartNumber(cmp.parmeters["Manufacturer"], cmp.parmeters["Comment"], ciivaClient)
        else:
            result = ciivaGetManufacturerComponentByPartNumber("", cmp.parmeters["Comment"], ciivaClient)
        
        #if len(result) == 1:
        #    ciivaComponentId = result[0]["ManufacturerComponentId"]
        #elif len(result) > 1:
        #    ciivaCmpList = []
        #    for i in xrange(len(result)):
        #        print result
                
        #        if result[i]["ManufacturerPartNumber"] == cmp.parmeters["Comment"]:
        #            cmpNameFullMatch = 1
        #            ciivaComponentId = result[i]["ManufacturerComponentId"]
        #            break
        #        else:
        #            ciivaCmpList.append(result[i]["ManufacturerPartNumber"] + " / " +result[i]["ManufacturerName"])
        #            cmpNameFullMatch = 0
            
        #    if not cmpNameFullMatch:
        #        print "multipled matches found, select one to match: " + cmp.parmeters["Comment"]
        #        print ""
        #        ciivaComponentId = result[selectItemInList(ciivaCmpList)]["ManufacturerComponentId"]
        #        ciivaClient = initCiivaConnection() #connect to ciiva again in case of time out suitation

        #else: ciivaComponentId = 0

        if result:
        #if ciivaComponentId:
            ciivaComponentId = result["ManufacturerComponentId"]
            #print ciivaComponentId
            paramResult = ciivaGetManufacturerComponentById(ciivaComponentId, ciivaClient)
            if paramResult.has_key("TechnicalDetails"):
                paramList = paramResult["TechnicalDetails"]
                for i in xrange(len(paramList)):
                    ciivaCmpParamsDict[cmp.parmeters["Comment"]][paramList[i]["Name"]] = paramList[i]["Value"]

    componentCount += 1
    #pb.progress(componentCount) 
                   
#crData = readCSVinOrder(crPath)
if ".csv" in crPath:
    crData = readCSVinOrder(crPath)
elif (".xls" in crPath):
    crData = readExcelFile(crPath)

for row in crData:
    if row.has_key("Component Name"):
        for cmp in ciivaCmpParamsDict:
            if row["Component Name"] == cmp:
                i = 1
                for paramName in ciivaCmpParamsDict[cmp]:
                    paramValue = ciivaCmpParamsDict[cmp][paramName]
                
                    row["Parameter " + str(i)] = paramName + ":" + paramValue
                    i += 1

writeDict2Excel(crPath, crData)

print ""
print "done"
#writeCSVDict(r"G:\cs.csv", crData)          