from cmpLib_ipy import *

vaultAddress = "http://shavault01.altium.biz:9780"
userName = "admin"
pwd = "admin"

pathList = r"G:\list.csv"

print "connecting to vault"
client = initVaultConnection(vaultAddress, userName, pwd)
print client.VaultInfo.HRID

folders = getVaultFolders(client)

folderList = readCSV(pathList)

for row in folderList:
    print row["Name"]
    createVaultFolder(row["Name"], folders, client)
