import cmpLib_ipy
import cmpLib_advanced_ipy
import xml.etree.ElementTree as ET

vaultAddress = "http://shavault01.altium.biz:9780"
userName = "admin"
pwd = "admin"
client = cmpLib_ipy.initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID
print client.PartCatalogUrl
print client.ServiceURL

revisions = cmpLib_ipy.getVaultComponentRevisionsByCompoentName(["TLV3012AIDCKR"], client)
for revision in revisions:
    cmpGuid = revision.ItemGUID
    print cmpGuid

cmpLib_ipy.releasePartChoice(client, cmpGuid, "TLV3012AIDCKR","TI")

#class dictClass:

#    def __init__(self, id = []):
#        print id
#        self.di = id

#for i in xrange(7):
#    di = dictClass()
#    di.di.append(i)
#print di.di

#def funcA():
#    x = "xx"
#    def funcAa():
#        print x

#    funcAa()
    

#funcA()

#class testObj():
#    attA = ""
#    attB = ""

#test = testObj()
#test.attA = "a"
#print test.attA

#vaultAddress = "http://vault.live.altium.com"
#userName = "hobart.content.center@altium.com"
#pwd = "Qwdntowo8"
#client = cmpLib_ipy.initVaultConnection(vaultAddress, userName, pwd)

#lifeCycles = client.GetLifeCycleDefinitions("")
#for lifeCycle in lifeCycles:
#    print lifeCycle.HRID + ":" +lifeCycle.GUID


#crFolder = r"G:\newcontentteam\Components\TIRequestSource\DatabaseLibraries - CmpLib\TI Release\Not updated files"
#recordList = cmpLib_ipy.traversalFolder(crFolder, "CmpLib")

#f = open("G:\\text.txt", "wb")
#r = open("G:\\error.txt", "wb")

#for cmpLibFile in recordList:
#    print cmpLibFile
#    try:
#        componentCollect = cmpLib_advanced_ipy.parseCmpLib(cmpLibFile)
#        for cmpDef in componentCollect.dataTables["ComponentDefinitions"].tableData:
#            cmpName = cmpDef.data["Comment"]
#            f.write(cmpName)
#            f.write("\r\n")
#            print cmpName
#    except Exception, e:
#        print str(e)
#        r.write(cmpLibFile)
#        r.write("\r\n")



#folders = cmpLib_ipy.getVaultFolders(client)

#cmpLib_ipy.createVaultFolder(r"2test\3rd\4th", folders, client)



#vaultAddress = "http://shacontent-vat.altium.biz:9780"
#userName = "admin"
#pwd = "admin"
#client = cmpLib_ipy.initVaultConnection(vaultAddress, userName, pwd)
#print client.VaultInfo.HRID


#cList = []
#cmp = cmpLib_ipy.component([],[],{},"")
#cmp.parmeters["Comment"] = "TAS2555YZR"
#cList.append(cmp)
#rev = cmpLib_ipy.getBatchVaultItemInfofromVault(client, cList, "CMPLIB")
#print len(rev)

#vaultAddress = "https://altiumvault.itg.ti.com:9785"
#userName = "x0223996"
#pwd = "Nf9jngfD"

#filePath = "G:\\temp check\\Fuse.CmpLib"
#pars = ET.XMLParser(encoding="utf-8")
##eleCmplib = ET.parse(filePath, parser=pars)
##ET.dump(eleCmplib)

#data = cmpLib_advanced_ipy.parseCmpLib(filePath)

#for param in data.dataTables["ParameterLinks"].tableData:
#    print param.data

#for cmp in data.dataTables["ComponentDefinitions"].tableData:
#    print cmp.data

#for t in data.dataTables:
#    print t
#    data.dataTables[t].printTable()

#eleData = cmpLib_advanced_ipy.buildCmplib(data.dataTables)
#cmpLib_advanced_ipy.writeEle2File(eleData, "G:\\temp check\\1.CmpLib")

#print "connecting to vault"


#folders = cmpLib_ipy.getVaultFolders(client)
#for folder in folders:
#    if folder.folderName == "Rgb":
#        print folder.guid + "|" + folder.parentFolderGUID
#        es = cmpLib_ipy.getFullPathbyFolderGUID(folder.guid, folders)
#        print es

#guid = cmpLib_ipy.getSpecificFolderGUID("Components", folders)

#print guid

#raw_input()

#errorReport = r"G:\error.txt"
#error = open(errorReport, "wb")
#hridList = cmpLib_ipy.re+		$exception	{"Local variable 'funcAa' referenced before assignment."}	System.Exception {IronPython.Runtime.UnboundLocalException}
#triveItemHRID("CMP-{0000000}", "74000", client, 100, "CMP")
#for i in hridList:
#    print i

#query = "HRID > 'CMP-0074000' and CONTENTTYPEGUID = 'CB3C11C4-E317-11DF-B822-12313F0024A2'"
#vaultItemList = client.GetItems(query)
#print vaultItemList.Count
#for item in vaultItemList:
#    print item.HRID
#    error.write(item.HRID)
#    error.write("\r\n")

#vaultAddress = "http://shavault01.altium.biz:9780"
#userName = "admin"
#pwd = "admin"
#client = cmpLib_ipy.initVaultConnection(vaultAddress, userName, pwd)
#print client.VaultInfo.HRID

#res = cmpLib_ipy.getVaultComponentRevisionsByLinkedModelName(["SOT-723"], "PCBLIB", client)