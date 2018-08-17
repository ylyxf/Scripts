#sort component partnumber and their new family data in a CR, check vault against this record
#if vault component is not in the correct folder, then move it

from cmpLib_ipy import *
import sys


config = configInfo()
config.readConfigFile("Config.ini")
vaultAddress = config.configDict["Vault Adddress"]
userName = config.configDict["User Name"]
pwd = config.configDict["Password"]
crPath = config.configDict["Component Records Folder"] + "\\" + config.configDict["Component Record"]
crType = config.configDict["Component Record Type"]

pathMask = r"Components\TI Components"
resultReport = open(r"G:\report.txt", "wb")
folderPathReport = open(r"G:\folderPath.txt", "wb")

print 'parsing component record'
if (crType == "Altium"):
    componentSet = parseAluCR(crPath)
else:
    componentSet = parseTIcr(crPath)


#clean up target vault folder path
componentSet.tarFolderPath = []
for cmp in componentSet.componentList:
    cmp.tarFolderPath = "Components\\TI Components\\Public\\" + cmp.tarFolderPath
    if cmp.tarFolderPath not in componentSet.tarFolderPath:
        componentSet.tarFolderPath.append(cmp.tarFolderPath)
        folderPathReport.write(cmp.tarFolderPath + "\r\n")
print "please check file folderPath.txt, then press enter to continue"
sys.stdin.readline()


print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

print "getting all folders in vault"
allFolders = getVaultFolders(client)
setLeafFolder(allFolders) #find all leaf folders and set mark

for folder in allFolders:
    if not folder.isLeaf:
        continue

    folderPath = getFullPathbyFolderGUID(folder.guid, allFolders)
    if not pathMask in folderPath:
        continue

    print "\r\nchecking components in", folderPath 
    itemList = getAllItemsInfoInSpecifiedFolder(client, folder.guid)
    moveDict = {}
    moveItemCount = 0
    checkingProgress = sys.stdout
   
    for item in itemList:
        matchedComponent = componentSet.hasComponent(item.Comment)
        if matchedComponent:
            tarFolderGUID = getSpecificFolderGUID(matchedComponent.tarFolderPath, allFolders)
            
            if not tarFolderGUID:
                try:
                    allFolders = createVaultFolder(matchedComponent.tarFolderPath, allFolders, client)
                    tarFolderGUID = getSpecificFolderGUID(matchedComponent.tarFolderPath, allFolders)
                    print tarFolderGUID

                    print "new folder created " + matchedComponent.tarFolderPath
                    resultReport.write("new folder created " + matchedComponent.tarFolderPath)
                    resultReport.write("\r\n")
                except Exception, e:
                    print e.Message
                    resultReport.write("folder creating failed, " + item.Comment + " not moved\r\n")
            
            if tarFolderGUID != item.FolderGUID:
                moveDict[item.ItemGUID] = tarFolderGUID
                moveItemCount = moveItemCount + 1
          
                checkingProgress.writelines(str(moveItemCount) + ' components will be moved\r')
                checkingProgress.flush()
       
                resultReport.write(item.Comment + " will be moved")
                resultReport.write("\r\n")

        else:
            #print item.Comment, "not found in record"
            resultReport.write(item.Comment + " not found in record\r\n")

    print  moveItemCount, 'components will be moved'

    if moveDict:
        print "moving components..."
        try:
            moveItems(moveDict,client)
        except Exception, e:
            print e.Message
            resultReport.write(e.Message)
            resultReport.write("\r\n")

print "done"

