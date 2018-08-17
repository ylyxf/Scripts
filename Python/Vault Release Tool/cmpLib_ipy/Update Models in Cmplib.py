# update models to the latest revsion

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

    for rowModelLink in cmplibData.dataTables["ModelLinks"].tableData:
        if rowModelLink.data["ItemGUID"]:
            revs = cl.getVaultItemRevisionByItemGUID(client, [rowModelLink.data["ItemGUID"]])
            if revs:
                latestRev = cl.getVaultItemRevisionInfoLatestRev(revs)[0]
                rowModelLink.data["RevisionGUID"] = latestRev.RevisionGUID
                rowModelLink.data["RevisionId"] = latestRev.RevisionID
                rowModelLink.data["HRID"] = latestRev.HRID

    eleData = cla.buildCmplib(cmplibData.dataTables)
    cla.writeEle2File(eleData, config.configDict["CmpLib Folder"] + "\\[Models Updated] " + cl.OP.basename(cmpLibFile) )

