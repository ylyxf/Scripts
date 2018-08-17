import cmpLib_advanced_ipy as cla
import cmpLib_ipy as cl

config = cl.configInfo()
config.readConfigFile("Config.ini")
cmpLibReocrdList = cl.traversalFolder(config.configDict["CmpLib Folder"], "CmpLib")

for cmpLibFile in cmpLibReocrdList:
    print cl.OP.basename(cmpLibFile)
    cmplibData = cla.parseCmpLib(cmpLibFile)

    rowDataReqParamDatashsetURL = cmplibData.dataTables["RequiredParameters"].lookupRow("HRID", "ComponentLink1URL")[0]
    ReqParamDatasheetURLId = rowDataReqParamDatashsetURL["refID"]
    
    for rowCmpDef in cmplibData.dataTables["ComponentDefinitions"].tableData:
        if rowCmpDef.data["Comment"]:
            rowsDataParam = cmplibData.dataTables["ParameterLinks"].lookupRow("RequiredParameter", ReqParamDatasheetURLId)
            for rowDataParam in rowsDataParam:
                if rowDataParam["Component"] == rowCmpDef.data["refID"]:
                    todo