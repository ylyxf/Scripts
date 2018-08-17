from cmpLib_ipy import *


#Move components in each vaul leaf folder. the target folders are sorted in movelist.csv, with two cloumn, Name and Folder
#Only the folders under Path Mask will checked

vaultAddress = "http://shavault01.altium.biz:9780"
userName = "frank"
pwd = "123"

pathMask = r"Components\TI Components\Public\Wireless Connectivity"

folderMatchList = r"G:\movelist.csv"
errorReport = r"G:\error.txt"

matchData = readCSV(folderMatchList)
error = open(errorReport, "wb")

print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)
setLeafFolder(allFolders) #find all leaf folders and set mark

for folder in allFolders:
    #assume components are only in leaf folders
    if folder.isLeaf:
        folderPath = getFullPathbyFolderGUID(folder.guid, allFolders)
        if pathMask in folderPath:
            print folderPath

            itemList = getAllItemsInfoInSpecifiedFolder(client,folder.guid) #get vault item info in each leaf folder under path mask
            moveDict = {}
            for item in itemList: #for each component, check against move list
                cmpFound = 0
                
                for row in matchData:
                    if row["Name"].strip() == item.Comment:
                        tarFolderGUID = getSpecificFolderGUID(row["Folder"], allFolders)

                        if not tarFolderGUID: #if the target folder is not existing, create it.
                            try:
                                createVaultFolder(row["Folder"], allFolders, client)
                                tarFolderGUID = getSpecificFolderGUID(row["Folder"], allFolders)
                                print "new folder created " + row["Folder"]
                                error.write(row["Folder"])
                                error.write("\r\n")
                            except Exception, e:
                                print e.Message
                                #str(error.write(e.Message)) + "|" + folderPath
                                #error.write("\r\n")

                        if tarFolderGUID:
                            moveDict[item.ItemGUID] = tarFolderGUID
                        cmpFound = 1
                        break

                if not cmpFound:
                    print "Component Not Found in List: " + item.Comment
                    error.write(item.Comment + "|" + folderPath)
                    error.write("\r\n")

            print "Moving Components..."
            try:
                moveItems(moveDict, client)
            except Exception, e:
                print e.Message
                #error.write(e.Message) + "|" + folderPath
                #error.write("\r\n")

                     

