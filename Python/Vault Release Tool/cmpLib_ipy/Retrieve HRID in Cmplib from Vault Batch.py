import cmpLib_advanced_ipy as cla
import cmpLib_ipy as cl

config = cl.configInfo()
config.readConfigFile("Config.ini")

vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]

cmpLibReocrdList = cl.traversalFolder(config.configDict["CmpLib Folder"], "CmpLib")

print "connecting to vault"
client = cl.initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

for cmpLibFile in cmpLibReocrdList:
    print cl.OP.basename(cmpLibFile)
    cmplibData = cla.parseCmpLib(cmpLibFile)

    pb = cl.progressbarClass(len(cmplibData.dataTables["ComponentDefinitions"].tableData), "*")
    cmpCount = 0
    for rowCmpDef in cmplibData.dataTables["ComponentDefinitions"].tableData:
        if rowCmpDef.data.has_key("Comment"):
            if rowCmpDef.data["Comment"]:
                vaultCmp = cl.component([],[],{"Comment":rowCmpDef.data["Comment"]}, "")
                vaultCmpRevs = cl.getVaultItemRevisionInfoLatestRev(client, [vaultCmp], "CMPLIB")
                for vaultCmpRev in vaultCmpRevs:
                    rowCmpDef.data["HRID"] = vaultCmpRev.HRID
                    rowCmpDef.data["ItemHRID"] = vaultCmpRev.HRID.rpartition("-")[0]
                    rowCmpDef.data["RevisionGUID"] = vaultCmpRev.RevisionGUID
                    rowCmpDef.data["GUID"] = vaultCmpRev.ItemGUID

        pb.progress(cmpCount + 1)
        cmpCount += 1

    eleData = cla.buildCmplib(cmplibData.dataTables)
    cla.writeEle2File(eleData, config.configDict["CmpLib Folder"] + "\\[HRID Updated] " + cl.OP.basename(cmpLibFile) )
    