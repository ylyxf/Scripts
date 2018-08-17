from cmpLib_ipy import *


#move duplicated parts to a folder

vaultAddress = "https://altiumvault.itg.ti.com:9785"
userName = "x0223996"
pwd = "Nf9jngfD"

pathMask = r"Managed Content\Models\sym"

errorReport = r"G:\error.txt"
error = open(errorReport, "wb")

print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)
#setLeafFolder(allFolders) #find all leaf folders and set mark

tarFolderGUID = getSpecificFolderGUID("Trash\Duplicated Symbols", allFolders)
print tarFolderGUID

nameDict = {}
duplicatedList = []
moveDict = {}
for folder in allFolders:
    #assume components are only in leaf folders
    if folder.isLeaf:
        folderPath = getFullPathbyFolderGUID(folder.guid, allFolders)
        if pathMask in folderPath:
            print folderPath

            itemList = getAllItemsInfoInSpecifiedFolder(client,folder.guid) #get vault item info in each leaf folder under path mask
            for item in itemList:
                if not nameDict.has_key(item.Comment):
                    nameDict[item.Comment] = item.ItemGUID
                else:
                    print item.Comment + " found duplicated"
                    moveDict[item.ItemGUID] = tarFolderGUID
                    if item.Comment not in duplicatedList:
                        moveDict[nameDict[item.Comment]] = tarFolderGUID
                        duplicatedList.append(item.Comment)
                        error.write(item.Comment)
                        error.write("\r\n")
                     
print "moving components..."
print moveDict
try:
    moveItems(moveDict, client)
except Exception, e:
    print e.Message
